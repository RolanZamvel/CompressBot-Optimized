"""
Telegram infrastructure services for CompressBot Optimized.

This module contains Telegram-specific implementations of
storage and notification services.
"""
from typing import Optional, Dict, Any
import os

from src.application.services import IFileStorageService, INotificationService


class TelegramFileStorageService(IFileStorageService):
    """Telegram file storage service implementation."""
    
    def __init__(self, app):
        self.app = app
    
    async def download_file(self, file_id: str, destination: str) -> bool:
        """Download a file from Telegram."""
        try:
            await self.app.download_media(file_id, file_name=destination)
            return os.path.exists(destination)
        except Exception:
            return False
    
    async def upload_file(self, file_path: str) -> str:
        """Upload a file to Telegram."""
        # This would be implemented for sending files back to users
        return file_path
    
    async def delete_file(self, file_path: str) -> bool:
        """Delete a file from local storage."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except Exception:
            return False
    
    def get_file_info(self, file_id: str) -> Optional[dict]:
        """Get file information from Telegram."""
        # Mock implementation
        return {
            'file_id': file_id,
            'file_size': 1024000,
            'mime_type': 'video/mp4'
        }


class TelegramNotificationService(INotificationService):
    """Telegram notification service implementation."""
    
    def __init__(self, app):
        self.app = app
    
    async def send_progress_update(
        self, 
        user_id: int, 
        job_id: str, 
        progress: int, 
        message: str
    ) -> None:
        """Send progress update to user."""
        try:
            progress_bar = "█" * (progress // 10) + "░" * (10 - progress // 10)
            await self.app.send_message(
                user_id,
                f"🔄 **Compression Progress**\n\n"
                f"📊 {progress_bar} {progress}%\n"
                f"📝 {message}"
            )
        except Exception:
            pass  # Ignore notification errors
    
    async def send_completion_notification(
        self, 
        user_id: int, 
        result
    ) -> None:
        """Send completion notification to user."""
        try:
            if result.success:
                await self.app.send_message(
                    user_id,
                    f"✅ **Compression Complete!**\n\n"
                    f"📊 Size reduced by {result.compression_percentage:.1f}%\n"
                    f"💾 Saved {result.size_reduction_mb:.1f} MB\n"
                    f"⏱️ Processing time: {result.processing_time:.1f}s"
                )
        except Exception:
            pass
    
    async def send_error_notification(
        self, 
        user_id: int, 
        error_message: str
    ) -> None:
        """Send error notification to user."""
        try:
            await self.app.send_message(
                user_id,
                f"❌ **Compression Failed**\n\n"
                f"📝 Error: {error_message}\n\n"
                f"Please try again or contact support."
            )
        except Exception:
            pass
