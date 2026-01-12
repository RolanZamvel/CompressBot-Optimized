"""
Main entry point for CompressBot Optimized.

This module contains the main application setup and dependency injection
container following SOLID principles.
"""
import asyncio
import sys
import os
from contextlib import asynccontextmanager
from typing import Dict, Any

from pyrogram import Client

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.interfaces.controllers.telegram_controller import TelegramBotController
from src.application.services import CompressionOrchestrator
from src.infrastructure.external.telegram_service import TelegramFileStorageService, TelegramNotificationService
from src.infrastructure.compression.audio_compression_service import AudioCompressionService
from src.infrastructure.compression.video_compression_service import VideoCompressionService
from src.infrastructure.external.youtube_service import YouTubeService
from src.shared.config import ConfigService
from src.shared.logging import get_logger, setup_logging
from src.shared.dependency_injection import DIContainer


class CompressBotApplication:
    """Main application class with dependency injection."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.di_container = DIContainer()
        self.app: Client = None
        self.controller: TelegramBotController = None
        
    async def initialize(self):
        """Initialize the application with all dependencies."""
        self.logger.info("Initializing CompressBot Optimized...")
        
        # Setup configuration
        config_service = ConfigService()
        self.di_container.register('config', config_service)
        
        # Setup logging
        setup_logging(config_service)
        
        # Create Pyrogram app
        telegram_config = config_service.get_telegram_config()
        self.app = Client(
            "compressbot_optimized",
            api_id=telegram_config.api_id,
            api_hash=telegram_config.api_hash,
            bot_token=telegram_config.bot_token,
            in_memory=True
        )
        
        # Register infrastructure services
        await self._register_infrastructure_services(config_service)
        
        # Register application services
        await self._register_application_services()
        
        # Create and register controller
        await self._register_controller()
        
        self.logger.info("Application initialized successfully")
    
    async def _register_infrastructure_services(self, config_service):
        """Register infrastructure services."""
        # File storage service
        file_storage = TelegramFileStorageService(self.app)
        self.di_container.register('file_storage', file_storage)
        
        # Notification service
        notification_service = TelegramNotificationService(self.app)
        self.di_container.register('notification_service', notification_service)
        
        # Compression services
        audio_compressor = AudioCompressionService(config_service)
        video_compressor = VideoCompressionService(config_service)
        self.di_container.register('audio_compressor', audio_compressor)
        self.di_container.register('video_compressor', video_compressor)
        
        # YouTube service
        youtube_service = YouTubeService(config_service)
        self.di_container.register('youtube_service', youtube_service)
    
    async def _register_application_services(self):
        """Register application services."""
        # Get dependencies
        file_storage = self.di_container.get('file_storage')
        notification_service = self.di_container.get('notification_service')
        logger = get_logger('CompressionOrchestrator')
        
        # Create compression orchestrator
        orchestrator = CompressionOrchestrator(
            compression_service=None,  # Will be set per media type
            file_storage=file_storage,
            notification_service=notification_service,
            job_repository=None,  # Memory repository for now
            logger=logger
        )
        self.di_container.register('compression_orchestrator', orchestrator)
    
    async def _register_controller(self):
        """Register the main controller."""
        orchestrator = self.di_container.get('compression_orchestrator')
        youtube_service = self.di_container.get('youtube_service')
        config_service = self.di_container.get('config')
        
        self.controller = TelegramBotController(
            app=self.app,
            compression_orchestrator=orchestrator,
            youtube_service=youtube_service,
            config_service=config_service
        )
    
    async def start(self):
        """Start the application."""
        self.logger.info("Starting CompressBot Optimized...")
        
        await self.initialize()
        
        # Start the bot
        await self.app.start()
        self.logger.info("Bot started successfully!")
        
        # Keep the bot running
        self.logger.info("CompressBot Optimized is running... Press Ctrl+C to stop.")
        
        try:
            # Keep the event loop running
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            self.logger.info("Received shutdown signal...")
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """Shutdown the application gracefully."""
        self.logger.info("Shutting down CompressBot Optimized...")
        
        if self.app:
            await self.app.stop()
        
        self.logger.info("Application shutdown complete")


async def main():
    """Main entry point."""
    app = CompressBotApplication()
    await app.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
