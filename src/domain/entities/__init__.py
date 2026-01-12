"""
Domain entities for CompressBot Optimized.

This module contains the core business entities that represent
the main concepts of the compression domain.
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from uuid import uuid4


class MediaType(Enum):
    """Enumeration of supported media types."""
    AUDIO = "audio"
    VIDEO = "video"
    ANIMATION = "animation"
    DOCUMENT = "document"
    IMAGE = "image"


class CompressionStatus(Enum):
    """Enumeration of compression process status."""
    PENDING = "pending"
    DOWNLOADING = "downloading"
    COMPRESSING = "compressing"
    UPLOADING = "uploading"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class QualityLevel(Enum):
    """Enumeration of quality levels for compression."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"
    CUSTOM = "custom"


@dataclass(frozen=True)
class MediaFile:
    """Represents a media file to be compressed."""
    file_id: str
    filename: Optional[str]
    file_size: int
    media_type: MediaType
    mime_type: str
    duration: Optional[int] = None  # Duration in seconds for audio/video
    width: Optional[int] = None
    height: Optional[int] = None
    bitrate: Optional[int] = None
    user_id: Optional[int] = None
    chat_id: Optional[int] = None
    message_id: Optional[int] = None
    
    def __post_init__(self):
        """Validate media file data."""
        if not self.file_id:
            raise ValueError("file_id is required")
        if self.file_size <= 0:
            raise ValueError("file_size must be positive")
        if not self.mime_type:
            raise ValueError("mime_type is required")


@dataclass(frozen=True)
class CompressionOptions:
    """Represents compression options for a media file."""
    quality_level: QualityLevel
    strategy: str
    custom_parameters: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate compression options."""
        if not self.strategy:
            raise ValueError("strategy is required")


@dataclass
class CompressionJob:
    """Represents a compression job in the system."""
    job_id: str
    media_file: MediaFile
    compression_options: CompressionOptions
    status: CompressionStatus
    progress: int = 0
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    output_file_path: Optional[str] = None
    original_size: int = 0
    compressed_size: int = 0
    compression_ratio: float = 0.0
    
    def __post_init__(self):
        """Initialize timestamps if not provided."""
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    def start_compression(self) -> None:
        """Mark the job as started."""
        self.status = CompressionStatus.COMPRESSING
        self.started_at = datetime.utcnow()
    
    def complete_compression(self, output_path: str, compressed_size: int) -> None:
        """Mark the job as completed."""
        self.status = CompressionStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.output_file_path = output_path
        self.compressed_size = compressed_size
        self.compression_ratio = (self.original_size - compressed_size) / self.original_size
        self.progress = 100
    
    def fail_compression(self, error_message: str) -> None:
        """Mark the job as failed."""
        self.status = CompressionStatus.FAILED
        self.completed_at = datetime.utcnow()
        self.error_message = error_message
    
    def update_progress(self, progress: int) -> None:
        """Update the progress of the compression."""
        self.progress = max(0, min(100, progress))
    
    def get_duration(self) -> Optional[float]:
        """Get the duration of the compression in seconds."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


@dataclass(frozen=True)
class User:
    """Represents a user in the system."""
    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    language_code: Optional[str] = None
    is_premium: bool = False
    created_at: datetime = None
    
    def __post_init__(self):
        """Validate user data."""
        if self.user_id <= 0:
            raise ValueError("user_id must be positive")
        if self.created_at is None:
            object.__setattr__(self, 'created_at', datetime.utcnow())
    
    @property
    def full_name(self) -> str:
        """Get the user's full name."""
        parts = []
        if self.first_name:
            parts.append(self.first_name)
        if self.last_name:
            parts.append(self.last_name)
        return " ".join(parts) if parts else "Unknown"
    
    @property
    def display_name(self) -> str:
        """Get the display name for the user."""
        if self.username:
            return f"@{self.username}"
        return self.full_name


@dataclass(frozen=True)
class CompressionResult:
    """Represents the result of a compression operation."""
    success: bool
    job_id: str
    output_path: Optional[str] = None
    original_size: int = 0
    compressed_size: int = 0
    compression_ratio: float = 0.0
    processing_time: float = 0.0
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate compression result."""
        if self.success and not self.output_path:
            raise ValueError("output_path is required when success is True")
        if not self.success and not self.error_message:
            raise ValueError("error_message is required when success is False")
    
    @property
    def size_reduction_mb(self) -> float:
        """Get the size reduction in megabytes."""
        return (self.original_size - self.compressed_size) / (1024 * 1024)
    
    @property
    def compression_percentage(self) -> float:
        """Get the compression percentage."""
        return self.compression_ratio * 100
