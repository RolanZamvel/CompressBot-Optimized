"""
Application services for CompressBot Optimized.

This module contains the service interfaces and implementations
for the application layer.
"""
from typing import List, Optional, Protocol, runtime_checkable
import os
import asyncio
from uuid import uuid4

from src.domain.entities import (
    MediaFile, CompressionJob, CompressionOptions, 
    CompressionResult, User, MediaType, QualityLevel, CompressionStatus
)


@runtime_checkable
class ICompressionService(Protocol):
    """Protocol for compression services."""
    
    async def compress(
        self,
        media_file: MediaFile,
        options: CompressionOptions,
        progress_callback: Optional[callable] = None
    ) -> CompressionResult:
        """Compress a media file."""
        ...


@runtime_checkable
class IFileStorageService(Protocol):
    """Protocol for file storage services."""
    
    async def download_file(self, file_id: str, destination: str) -> bool:
        """Download a file from storage."""
        ...
    
    async def upload_file(self, file_path: str) -> str:
        """Upload a file to storage."""
        ...
    
    async def delete_file(self, file_path: str) -> bool:
        """Delete a file from storage."""
        ...
    
    def get_file_info(self, file_id: str) -> Optional[dict]:
        """Get file information."""
        ...


@runtime_checkable
class INotificationService(Protocol):
    """Protocol for notification services."""
    
    async def send_progress_update(
        self, 
        user_id: int, 
        job_id: str, 
        progress: int, 
        message: str
    ) -> None:
        """Send progress update to user."""
        ...
    
    async def send_completion_notification(
        self, 
        user_id: int, 
        result: CompressionResult
    ) -> None:
        """Send completion notification to user."""
        ...
    
    async def send_error_notification(
        self, 
        user_id: int, 
        error_message: str
    ) -> None:
        """Send error notification to user."""
        ...


@runtime_checkable
class IJobRepository(Protocol):
    """Protocol for job repository."""
    
    async def save_job(self, job: CompressionJob) -> CompressionJob:
        """Save a compression job."""
        ...
    
    async def get_job(self, job_id: str) -> Optional[CompressionJob]:
        """Get a compression job by ID."""
        ...
    
    async def get_user_jobs(self, user_id: int) -> List[CompressionJob]:
        """Get all jobs for a user."""
        ...
    
    async def update_job(self, job: CompressionJob) -> CompressionJob:
        """Update a compression job."""
        ...
    
    async def delete_job(self, job_id: str) -> bool:
        """Delete a compression job."""
        ...


class CompressionOrchestrator:
    """Orchestrates the compression workflow."""
    
    def __init__(
        self,
        compression_service: ICompressionService,
        file_storage: IFileStorageService,
        notification_service: INotificationService,
        job_repository: IJobRepository,
        logger
    ):
        self.compression_service = compression_service
        self.file_storage = file_storage
        self.notification_service = notification_service
        self.job_repository = job_repository
        self.logger = logger
    
    async def process_compression_request(
        self, 
        media_file: MediaFile, 
        options: CompressionOptions
    ) -> CompressionResult:
        """Process a compression request from start to finish."""
        job = CompressionJob(
            job_id=str(uuid4()),
            media_file=media_file,
            compression_options=options,
            status=CompressionStatus.PENDING,
            original_size=media_file.file_size
        )
        
        # Save job
        job = await self.job_repository.save_job(job)
        self.logger.info(f"Started compression job {job.job_id}")
        
        try:
            # Update status to downloading
            job.status = CompressionStatus.DOWNLOADING
            await self.job_repository.update_job(job)
            
            # Download file
            temp_path = f"/tmp/{job.job_id}_{media_file.filename or 'file'}"
            if not await self.file_storage.download_file(media_file.file_id, temp_path):
                raise Exception("Failed to download file")
            
            # Update status to compressing
            job.status = CompressionStatus.COMPRESSING
            job.start_compression()
            await self.job_repository.update_job(job)
            
            # For now, return a mock result
            result = CompressionResult(
                success=True,
                job_id=job.job_id,
                output_path=temp_path,
                original_size=media_file.file_size,
                compressed_size=int(media_file.file_size * 0.7),  # Mock 30% compression
                compression_ratio=0.3,
                processing_time=5.0
            )
            
            # Complete job
            job.complete_compression(result.output_path, result.compressed_size)
            await self.job_repository.update_job(job)
            
            # Send notification
            await self.notification_service.send_completion_notification(
                media_file.user_id, result
            )
            
            self.logger.info(f"Completed compression job {job.job_id}")
            return result
            
        except Exception as e:
            job.fail_compression(str(e))
            await self.job_repository.update_job(job)
            
            await self.notification_service.send_error_notification(
                media_file.user_id, str(e)
            )
            
            self.logger.error(f"Error in compression job {job.job_id}: {str(e)}")
            
            return CompressionResult(
                success=False,
                job_id=job.job_id,
                error_message=str(e)
            )
        
        finally:
            # Cleanup temp files
            await self._cleanup_temp_files(temp_path)
    
    async def _handle_progress(self, job: CompressionJob, progress: int) -> None:
        """Handle progress updates."""
        job.update_progress(progress)
        await self.job_repository.update_job(job)
        await self.notification_service.send_progress_update(
            job.media_file.user_id,
            job.job_id,
            progress,
            f"Compression progress: {progress}%"
        )
    
    async def _cleanup_temp_files(self, *paths: str) -> None:
        """Clean up temporary files."""
        for path in paths:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as e:
                    self.logger.warning(f"Failed to cleanup temp file {path}: {e}")
