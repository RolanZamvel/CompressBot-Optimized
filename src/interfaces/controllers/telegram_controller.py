"""
Telegram Bot Controller for CompressBot Optimized.

This module contains the Telegram bot controller that handles
incoming messages and orchestrates the compression workflow.
"""
import asyncio
import re
from typing import Optional, Dict, Any

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from src.domain.entities import (
    MediaFile, MediaType, CompressionOptions, 
    QualityLevel, User
)
from src.application.services import CompressionOrchestrator
from src.shared.logging import get_logger


class TelegramBotController:
    """Telegram bot controller with SOLID principles."""
    
    def __init__(
        self,
        app: Client,
        compression_orchestrator: CompressionOrchestrator,
        youtube_service,
        config_service
    ):
        self.app = app
        self.compression_orchestrator = compression_orchestrator
        self.youtube_service = youtube_service
        self.config_service = config_service
        self.logger = get_logger(__name__)
        
        # User context storage
        self.user_context: Dict[int, Dict[str, Any]] = {}
        
        # YouTube URL regex
        self.youtube_regex = re.compile(
            r'(https?://)?(www\.)?(youtube\.com/(watch\?v=|shorts/)|youtu\.be/)[\w-]+'
        )
        
        self._register_handlers()
    
    def _register_handlers(self):
        """Register all bot handlers."""
        
        @self.app.on_message(filters.command("start"))
        async def start_command(client: Client, message: Message):
            """Handle /start command."""
            await self._handle_start_command(message)
        
        @self.app.on_message(filters.command("help"))
        async def help_command(client: Client, message: Message):
            """Handle /help command."""
            await self._handle_help_command(message)
        
        @self.app.on_message(filters.command("status"))
        async def status_command(client: Client, message: Message):
            """Handle /status command."""
            await self._handle_status_command(message)
        
        @self.app.on_message(filters.audio | filters.voice)
        async def audio_message(client: Client, message: Message):
            """Handle audio messages."""
            await self._handle_audio_message(message)
        
        @self.app.on_message(filters.video | filters.animation)
        async def video_message(client: Client, message: Message):
            """Handle video messages."""
            await self._handle_video_message(message)
        
        @self.app.on_message(filters.text)
        async def text_message(client: Client, message: Message):
            """Handle text messages (YouTube URLs)."""
            await self._handle_text_message(message)
        
        @self.app.on_callback_query()
        async def callback_query(client: Client, callback: CallbackQuery):
            """Handle callback queries."""
            await self._handle_callback_query(callback)
    
    async def _handle_start_command(self, message: Message):
        """Handle /start command."""
        try:
            user = self._create_user_from_message(message)
            
            markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🎧 Compress Audio", callback_data="compress_audio"),
                    InlineKeyboardButton("🎥 Compress Video", callback_data="compress_video")
                ],
                [
                    InlineKeyboardButton("📺 YouTube Downloader", callback_data="youtube_help"),
                    InlineKeyboardButton("❓ Help", callback_data="help")
                ]
            ])
            
            welcome_text = (
                "🤖 **Welcome to CompressBot Optimized!**\n\n"
                "I can compress your audio and video files with high quality "
                "using advanced SOLID architecture.\n\n"
                "📋 **Features:**\n"
                "• Audio compression (voice & files)\n"
                "• Video compression with quality options\n"
                "• YouTube video downloading\n"
                "• Real-time progress tracking\n"
                "• Clean architecture with SOLID principles\n\n"
                "Choose an option below to get started:"
            )
            
            await message.reply_text(welcome_text, reply_markup=markup)
            self.logger.info(f"User {user.user_id} started the bot")
            
        except Exception as e:
            self.logger.error(f"Error in start command: {str(e)}")
            await message.reply_text("❌ Sorry, an error occurred. Please try again.")
    
    async def _handle_help_command(self, message: Message):
        """Handle /help command."""
        help_text = (
            "📖 **CompressBot Optimized Help**\n\n"
            "**🎧 Audio Compression:**\n"
            "• Send any audio file or voice message\n"
            "• Automatic compression to optimal size\n"
            "• Maintains good quality\n\n"
            "**🎥 Video Compression:**\n"
            "• Send video files or animations\n"
            "• Choose quality level:\n"
            "  - 📊 Compress (smaller size)\n"
            "  - 🎬 Maintain Quality (larger size)\n\n"
            "**📺 YouTube Downloader:**\n"
            "• Send YouTube video URL\n"
            "• Choose format and quality\n"
            "• Download and compress\n\n"
            "**📊 Status Commands:**\n"
            "• /status - Check bot status\n"
            "• /help - Show this help\n\n"
            "**🏗️ Architecture:**\n"
            "Built with SOLID principles for maximum reliability "
            "and maintainability."
        )
        
        await message.reply_text(help_text)
    
    async def _handle_status_command(self, message: Message):
        """Handle /status command."""
        status_text = (
            "🤖 **Bot Status**\n\n"
            "✅ **Status:** Online\n"
            "🏗️ **Architecture:** SOLID Principles\n"
            "📦 **Version:** 2.0.0 Optimized\n"
            "🔧 **Features:** Audio, Video, YouTube\n\n"
            "Ready to compress your files! 🚀"
        )
        
        await message.reply_text(status_text)
    
    async def _handle_audio_message(self, message: Message):
        """Handle audio messages."""
        try:
            user = self._create_user_from_message(message)
            
            # Create media file entity
            media_file = MediaFile(
                file_id=message.audio.file_id if message.audio else message.voice.file_id,
                filename=message.audio.file_name if message.audio else f"voice_{message.id}.ogg",
                file_size=message.audio.file_size if message.audio else message.voice.file_size,
                media_type=MediaType.AUDIO,
                mime_type=message.audio.mime_type if message.audio else "audio/ogg",
                duration=message.audio.duration if message.audio else message.voice.duration,
                user_id=user.user_id,
                chat_id=message.chat.id,
                message_id=message.id
            )
            
            # Create compression options
            options = CompressionOptions(
                quality_level=QualityLevel.MEDIUM,
                strategy="balanced"
            )
            
            # Send processing message
            processing_msg = await message.reply_text(
                "🎧 **Processing audio...**\n\n"
                "📥 Downloading file...\n"
                "⏳ This may take a few moments."
            )
            
            # Process compression
            result = await self.compression_orchestrator.process_compression_request(
                media_file, options
            )
            
            # Update message with result
            if result.success:
                await processing_msg.edit_text(
                    f"✅ **Audio compressed successfully!**\n\n"
                    f"📊 **Compression Stats:**\n"
                    f"• Original: {result.original_size / (1024*1024):.1f} MB\n"
                    f"• Compressed: {result.compressed_size / (1024*1024):.1f} MB\n"
                    f"• Saved: {result.size_reduction_mb:.1f} MB ({result.compression_percentage:.1f}%)\n"
                    f"⏱️ Time: {result.processing_time:.1f}s"
                )
            else:
                await processing_msg.edit_text(
                    f"❌ **Compression failed**\n\n"
                    f"Error: {result.error_message}"
                )
                
        except Exception as e:
            self.logger.error(f"Error handling audio message: {str(e)}")
            await message.reply_text("❌ Sorry, an error occurred while processing your audio.")
    
    async def _handle_video_message(self, message: Message):
        """Handle video messages."""
        try:
            user = self._create_user_from_message(message)
            
            # Create media file entity
            media_file = MediaFile(
                file_id=message.video.file_id if message.video else message.animation.file_id,
                filename=message.video.file_name if message.video else f"animation_{message.id}.mp4",
                file_size=message.video.file_size if message.video else message.animation.file_size,
                media_type=MediaType.VIDEO if message.video else MediaType.ANIMATION,
                mime_type=message.video.mime_type if message.video else "video/mp4",
                duration=message.video.duration if message.video else None,
                width=message.video.width if message.video else message.animation.width,
                height=message.video.height if message.video else message.animation.height,
                user_id=user.user_id,
                chat_id=message.chat.id,
                message_id=message.id
            )
            
            # For animations, process directly
            if media_file.media_type == MediaType.ANIMATION:
                options = CompressionOptions(
                    quality_level=QualityLevel.MEDIUM,
                    strategy="animation"
                )
                await self._process_video_compression(message, media_file, options)
                return
            
            # For videos, show quality options
            file_size_mb = media_file.file_size / (1024 * 1024)
            estimated_time = max(10, int(file_size_mb * 1.5))
            
            markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "📊 Compress (smaller size)", 
                        callback_data=f"video_compress_{media_file.file_id}"
                    ),
                    InlineKeyboardButton(
                        "🎬 Maintain Quality", 
                        callback_data=f"video_quality_{media_file.file_id}"
                    )
                ]
            ])
            
            # Store context for callback
            self.user_context[user.user_id] = {
                'media_file': media_file,
                'message': message
            }
            
            status_text = (
                f"📥 **Video received** ({file_size_mb:.1f} MB)\n\n"
                f"⏱️ **Estimated time:** ~{estimated_time}s\n\n"
                f"🎯 **Choose compression quality:**"
            )
            
            await message.reply_text(status_text, reply_markup=markup)
            
        except Exception as e:
            self.logger.error(f"Error handling video message: {str(e)}")
            await message.reply_text("❌ Sorry, an error occurred while processing your video.")
    
    async def _handle_text_message(self, message: Message):
        """Handle text messages for YouTube URLs."""
        try:
            text = message.text.strip()
            
            # Check if it's a YouTube URL
            if self.youtube_service.is_youtube_url(text):
                await self._handle_youtube_url(message, text)
            
        except Exception as e:
            self.logger.error(f"Error handling text message: {str(e)}")
    
    async def _handle_youtube_url(self, message: Message, url: str):
        """Handle YouTube URL."""
        try:
            user = self._create_user_from_message(message)
            
            # Extract video info
            info = await self.youtube_service.extract_info(url)
            
            markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "📥 Download (Best Quality)", 
                        callback_data=f"youtube_download_{url}_best"
                    ),
                    InlineKeyboardButton(
                        "📥 Download (Compressed)", 
                        callback_data=f"youtube_download_{url}_compressed"
                    )
                ],
                [
                    InlineKeyboardButton("❌ Cancel", callback_data="youtube_cancel")
                ]
            ])
            
            # Store context
            self.user_context[user.user_id] = {
                'youtube_url': url,
                'video_info': info,
                'message': message
            }
            
            text = (
                f"📺 **YouTube Video Detected**\n\n"
                f"🎬 **Title:** {info.get('title', 'Unknown')}\n"
                f"⏱️ **Duration:** {info.get('duration', 'Unknown')}\n"
                f"👀 **Views:** {info.get('view_count', 'Unknown'):,}\n\n"
                f"🎯 **Choose download option:**"
            )
            
            await message.reply_text(text, reply_markup=markup)
            
        except Exception as e:
            self.logger.error(f"Error handling YouTube URL: {str(e)}")
            await message.reply_text("❌ Sorry, couldn't process that YouTube URL.")
    
    async def _handle_callback_query(self, callback: CallbackQuery):
        """Handle callback queries."""
        try:
            data = callback.data
            user_id = callback.from_user.id
            
            if data == "compress_audio":
                await self._handle_audio_help_callback(callback)
            elif data == "compress_video":
                await self._handle_video_help_callback(callback)
            elif data.startswith("video_compress_"):
                await self._handle_video_compress_callback(callback)
            elif data.startswith("video_quality_"):
                await self._handle_video_quality_callback(callback)
            elif data.startswith("youtube_download_"):
                await self._handle_youtube_download_callback(callback)
            elif data == "youtube_cancel":
                await self._handle_youtube_cancel_callback(callback)
            else:
                await callback.message.reply_text("Send me a file to compress!")
                
        except Exception as e:
            self.logger.error(f"Error handling callback query: {str(e)}")
            await callback.message.reply_text("❌ Sorry, an error occurred.")
    
    async def _handle_video_compress_callback(self, callback: CallbackQuery):
        """Handle video compress callback."""
        user_id = callback.from_user.id
        context = self.user_context.get(user_id)
        
        if not context:
            await callback.message.edit_text("❌ Session expired. Please send the file again.")
            return
        
        media_file = context['media_file']
        options = CompressionOptions(
            quality_level=QualityLevel.MEDIUM,
            strategy="size_reduction"
        )
        
        await callback.message.edit_text("🔄 **Compressing video for smaller size...**")
        await self._process_video_compression(context['message'], media_file, options)
        
        # Clean up context
        del self.user_context[user_id]
    
    async def _handle_video_quality_callback(self, callback: CallbackQuery):
        """Handle video quality callback."""
        user_id = callback.from_user.id
        context = self.user_context.get(user_id)
        
        if not context:
            await callback.message.edit_text("❌ Session expired. Please send the file again.")
            return
        
        media_file = context['media_file']
        options = CompressionOptions(
            quality_level=QualityLevel.HIGH,
            strategy="quality_preservation"
        )
        
        await callback.message.edit_text("🔄 **Compressing video with quality preservation...**")
        await self._process_video_compression(context['message'], media_file, options)
        
        # Clean up context
        del self.user_context[user_id]
    
    async def _process_video_compression(self, message: Message, media_file: MediaFile, options: CompressionOptions):
        """Process video compression."""
        try:
            processing_msg = await message.reply_text("🎥 **Processing video...**\n\n📥 Compressing...")
            
            result = await self.compression_orchestrator.process_compression_request(
                media_file, options
            )
            
            if result.success:
                await processing_msg.edit_text(
                    f"✅ **Video compressed successfully!**\n\n"
                    f"📊 **Compression Stats:**\n"
                    f"• Original: {result.original_size / (1024*1024):.1f} MB\n"
                    f"• Compressed: {result.compressed_size / (1024*1024):.1f} MB\n"
                    f"• Saved: {result.size_reduction_mb:.1f} MB ({result.compression_percentage:.1f}%)\n"
                    f"⏱️ Time: {result.processing_time:.1f}s"
                )
            else:
                await processing_msg.edit_text(
                    f"❌ **Compression failed**\n\n"
                    f"Error: {result.error_message}"
                )
                
        except Exception as e:
            self.logger.error(f"Error in video compression: {str(e)}")
            await message.reply_text("❌ Sorry, an error occurred during video compression.")
    
    def _create_user_from_message(self, message: Message) -> User:
        """Create User entity from message."""
        return User(
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language_code=message.from_user.language_code
        )
    
    async def _handle_audio_help_callback(self, callback: CallbackQuery):
        """Handle audio help callback."""
        text = (
            "🎧 **Audio Compression**\n\n"
            "Simply send me any audio file or voice message and "
            "I'll compress it automatically while maintaining good quality.\n\n"
            "**Supported formats:**\n"
            "• MP3, M4A, FLAC, WAV, OGG\n"
            "• Voice messages\n\n"
            "Send a file to get started! 🎵"
        )
        await callback.message.edit_text(text)
    
    async def _handle_video_help_callback(self, callback: CallbackQuery):
        """Handle video help callback."""
        text = (
            "🎥 **Video Compression**\n\n"
            "Send me any video file and I'll show you quality options:\n\n"
            "**📊 Compress:** Smaller file size, good quality\n"
            "**🎬 Maintain Quality:** Larger file, best quality\n\n"
            "**Supported formats:**\n"
            "• MP4, AVI, MOV, MKV, WebM\n"
            "• GIF animations\n\n"
            "Send a video to get started! 🎬"
        )
        await callback.message.edit_text(text)
    
    async def _handle_youtube_download_callback(self, callback: CallbackQuery):
        """Handle YouTube download callback."""
        await callback.message.edit_text("🔄 **Downloading from YouTube...**\n\nThis may take a moment...")
        # Implementation would go here
        # For now, just show a placeholder
        await asyncio.sleep(2)
        await callback.message.edit_text("📺 **YouTube download feature coming soon!**\n\nThis feature is under development.")
    
    async def _handle_youtube_cancel_callback(self, callback: CallbackQuery):
        """Handle YouTube cancel callback."""
        user_id = callback.from_user.id
        if user_id in self.user_context:
            del self.user_context[user_id]
        await callback.message.edit_text("❌ **Cancelled**")
