"""Telegram bot integration for content approval."""

import os
from typing import Optional, Callable
from pathlib import Path

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from .logger import get_logger

logger = get_logger()


class TelegramBot:
    """Handle Telegram bot operations for content approval."""
    
    def __init__(self, bot_token: str, user_id: int):
        """
        Initialize Telegram bot.
        
        Args:
            bot_token: Telegram bot token
            user_id: Telegram user ID to send messages to
        """
        self.bot_token = bot_token
        self.user_id = user_id
        self.application = None
        self.approval_callback = None
        self.rejection_callback = None
        logger.info(f"Telegram bot initialized for user: {user_id}")
    
    def set_approval_callback(self, callback: Callable):
        """Set callback function for approval action."""
        self.approval_callback = callback
    
    def set_rejection_callback(self, callback: Callable):
        """Set callback function for rejection action."""
        self.rejection_callback = callback
    
    async def send_video_for_approval(
        self,
        video_path: str,
        caption: str,
        video_id: str = None
    ) -> bool:
        """
        Send video to user for approval.
        
        Args:
            video_path: Path to video file
            caption: Instagram caption text
            video_id: Unique identifier for this video
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.application is None:
                self.application = Application.builder().token(self.bot_token).build()
            
            # Create inline keyboard with approval buttons
            keyboard = [
                [
                    InlineKeyboardButton("✅ Одобрить", callback_data=f"approve_{video_id}"),
                    InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{video_id}")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Prepare message
            message = f"📹 Новое видео для одобрения\n\n"
            message += f"📝 Подпись для Instagram:\n{caption}\n\n"
            message += "Пожалуйста, просмотрите видео и выберите действие:"
            
            # Send video
            with open(video_path, 'rb') as video_file:
                await self.application.bot.send_video(
                    chat_id=self.user_id,
                    video=video_file,
                    caption=message,
                    reply_markup=reply_markup,
                    supports_streaming=True
                )
            
            logger.info(f"Video sent for approval to user {self.user_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error sending video for approval: {e}")
            return False
    
    async def handle_approval(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle approval button callback."""
        query = update.callback_query
        await query.answer()
        
        # Extract video ID from callback data
        video_id = query.data.replace("approve_", "")
        
        await query.edit_message_caption(
            caption=f"✅ Видео одобрено!\n\n{query.message.caption}"
        )
        
        logger.info(f"Video {video_id} approved by user")
        
        # Call approval callback if set
        if self.approval_callback:
            self.approval_callback(video_id)
    
    async def handle_rejection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle rejection button callback."""
        query = update.callback_query
        await query.answer()
        
        # Extract video ID from callback data
        video_id = query.data.replace("reject_", "")
        
        await query.edit_message_caption(
            caption=f"❌ Видео отклонено\n\n{query.message.caption}"
        )
        
        logger.info(f"Video {video_id} rejected by user")
        
        # Call rejection callback if set
        if self.rejection_callback:
            self.rejection_callback(video_id)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        await update.message.reply_text(
            "👋 Привет! Я бот для одобрения видео контента отеля Atlas Apart.\n\n"
            "Я буду отправлять вам готовые видео для проверки и одобрения перед публикацией в Instagram."
        )
    
    def run_webhook(self, webhook_url: str, port: int = 8443):
        """
        Run bot with webhook (for production).
        
        Args:
            webhook_url: Public webhook URL
            port: Port to listen on
        """
        try:
            if self.application is None:
                self.application = Application.builder().token(self.bot_token).build()
            
            # Add handlers
            self.application.add_handler(CommandHandler("start", self.start_command))
            self.application.add_handler(
                CallbackQueryHandler(self.handle_approval, pattern="^approve_")
            )
            self.application.add_handler(
                CallbackQueryHandler(self.handle_rejection, pattern="^reject_")
            )
            
            # Run with webhook
            self.application.run_webhook(
                listen="0.0.0.0",
                port=port,
                url_path=self.bot_token,
                webhook_url=f"{webhook_url}/{self.bot_token}"
            )
            
            logger.info(f"Bot started with webhook: {webhook_url}")
        
        except Exception as e:
            logger.error(f"Error running bot with webhook: {e}")
    
    def run_polling(self):
        """Run bot with polling (for development/testing)."""
        try:
            if self.application is None:
                self.application = Application.builder().token(self.bot_token).build()
            
            # Add handlers
            self.application.add_handler(CommandHandler("start", self.start_command))
            self.application.add_handler(
                CallbackQueryHandler(self.handle_approval, pattern="^approve_")
            )
            self.application.add_handler(
                CallbackQueryHandler(self.handle_rejection, pattern="^reject_")
            )
            
            # Run with polling
            logger.info("Bot started with polling")
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)
        
        except Exception as e:
            logger.error(f"Error running bot with polling: {e}")
    
    async def send_message(self, message: str) -> bool:
        """
        Send a text message to user.
        
        Args:
            message: Message text
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.application is None:
                self.application = Application.builder().token(self.bot_token).build()
            
            await self.application.bot.send_message(
                chat_id=self.user_id,
                text=message
            )
            
            logger.info(f"Message sent to user {self.user_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False


# Helper function to send video without running bot
async def send_video_simple(
    bot_token: str,
    user_id: int,
    video_path: str,
    caption: str
) -> bool:
    """
    Send video to Telegram user (simple version without approval buttons).
    
    Args:
        bot_token: Telegram bot token
        user_id: Telegram user ID
        video_path: Path to video file
        caption: Video caption
        
    Returns:
        True if successful, False otherwise
    """
    try:
        from telegram import Bot
        
        bot = Bot(token=bot_token)
        
        # Create inline keyboard with approval buttons
        keyboard = [
            [
                InlineKeyboardButton("✅ Одобрить", callback_data="approve"),
                InlineKeyboardButton("❌ Отклонить", callback_data="reject")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Prepare message
        message = f"📹 Новое видео для одобрения\n\n"
        message += f"📝 Подпись для Instagram:\n{caption}\n\n"
        message += "Пожалуйста, просмотрите видео и выберите действие:"
        
        # Send video
        with open(video_path, 'rb') as video_file:
            await bot.send_video(
                chat_id=user_id,
                video=video_file,
                caption=message,
                reply_markup=reply_markup,
                supports_streaming=True
            )
        
        logger.info(f"Video sent successfully to user {user_id}")
        return True
    
    except Exception as e:
        logger.error(f"Error sending video: {e}")
        return False
