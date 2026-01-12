"""
Configuration service for CompressBot Optimized.

This module provides centralized configuration management
with environment variable support and validation.
"""
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class TelegramConfig:
    """Telegram configuration."""
    api_id: int
    api_hash: str
    bot_token: str


@dataclass
class CompressionConfig:
    """Compression configuration."""
    audio_bitrate: str = "32k"
    audio_format: str = "mp3"
    audio_channels: int = 1
    audio_sample_rate: int = 44100
    
    video_scale: str = "640:360"
    video_fps: int = 24
    video_codec: str = "libx265"
    video_bitrate: str = "100k"
    video_crf: int = 30
    video_preset: str = "ultrafast"
    video_pixel_format: str = "yuv420p"
    
    max_file_size_mb: int = 100
    temp_dir: str = "/tmp"


class ConfigService:
    """Configuration service with environment variable support."""
    
    def __init__(self):
        self._config_cache: Dict[str, Any] = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        if key in self._config_cache:
            return self._config_cache[key]
        
        # Try environment variable first
        env_value = os.getenv(key.upper())
        if env_value is not None:
            self._config_cache[key] = env_value
            return env_value
        
        # Return default
        return default
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config_cache[key] = value
    
    def get_telegram_config(self) -> TelegramConfig:
        """Get Telegram configuration."""
        api_id = self.get('API_ID')
        api_hash = self.get('API_HASH')
        bot_token = self.get('API_TOKEN')
        
        # Fallback to default values for development
        if not api_id:
            api_id = 12345678  # Default for development
        if not api_hash:
            api_hash = "default_api_hash_for_development"
        if not bot_token:
            bot_token = "default_bot_token_for_development"
        
        return TelegramConfig(
            api_id=int(api_id),
            api_hash=api_hash,
            bot_token=bot_token
        )
    
    def get_compression_config(self) -> CompressionConfig:
        """Get compression configuration."""
        return CompressionConfig(
            audio_bitrate=self.get('AUDIO_BITRATE', '32k'),
            audio_format=self.get('AUDIO_FORMAT', 'mp3'),
            audio_channels=int(self.get('AUDIO_CHANNELS', '1')),
            audio_sample_rate=int(self.get('AUDIO_SAMPLE_RATE', '44100')),
            
            video_scale=self.get('VIDEO_SCALE', '640:360'),
            video_fps=int(self.get('VIDEO_FPS', '24')),
            video_codec=self.get('VIDEO_CODEC', 'libx265'),
            video_bitrate=self.get('VIDEO_BITRATE', '100k'),
            video_crf=int(self.get('VIDEO_CRF', '30')),
            video_preset=self.get('VIDEO_PRESET', 'ultrafast'),
            video_pixel_format=self.get('VIDEO_PIXEL_FORMAT', 'yuv420p'),
            
            max_file_size_mb=int(self.get('MAX_FILE_SIZE_MB', '100')),
            temp_dir=self.get('TEMP_DIR', '/tmp')
        )
    
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.get('ENVIRONMENT', 'development').lower() == 'development'
    
    def get_log_level(self) -> str:
        """Get log level."""
        return self.get('LOG_LEVEL', 'INFO')
