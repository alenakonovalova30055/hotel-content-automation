import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError, NetworkError, TimedOut
from src.logger import logger

class TelegramHandler:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.user_id = os.getenv('TELEGRAM_USER_ID')
        self.bot = Bot(token=self.token)
        self.max_retries = 3
        self.retry_delay = 2  # seconds
    
    async def send_message(self, text: str) -> bool:
        """
        Send a message to Telegram with retry logic
        
        Args:
            text: Message text to send
            
        Returns:
            True if message was sent successfully, False otherwise
        """
        for attempt in range(self.max_retries):
            try:
                await self.bot.send_message(chat_id=self.user_id, text=text)
                logger.info(f"✅ Сообщение отправлено в Telegram")
                return True
            except (NetworkError, TimedOut) as e:
                if attempt < self.max_retries - 1:
                    logger.warning(f"⚠️ Ошибка сети Telegram (попытка {attempt + 1}/{self.max_retries}): {e}")
                    await asyncio.sleep(self.retry_delay)
                else:
                    logger.error(f"❌ Не удалось отправить сообщение после {self.max_retries} попыток: {e}")
                    return False
            except TelegramError as e:
                logger.error(f"❌ Ошибка Telegram: {e}")
                return False
            except Exception as e:
                logger.error(f"❌ Неожиданная ошибка при отправке сообщения: {e}")
                return False
        
        return False
    
    async def send_video(self, video_path: str, caption: str = "") -> bool:
        """
        Send a video to Telegram with retry logic
        
        Args:
            video_path: Path to the video file
            caption: Optional caption for the video
            
        Returns:
            True if video was sent successfully, False otherwise
        """
        for attempt in range(self.max_retries):
            try:
                with open(video_path, 'rb') as video_file:
                    await self.bot.send_video(
                        chat_id=self.user_id,
                        video=video_file,
                        caption=caption
                    )
                logger.info(f"✅ Видео отправлено в Telegram")
                return True
            except (NetworkError, TimedOut) as e:
                if attempt < self.max_retries - 1:
                    logger.warning(f"⚠️ Ошибка сети при отправке видео (попытка {attempt + 1}/{self.max_retries}): {e}")
                    await asyncio.sleep(self.retry_delay)
                else:
                    logger.error(f"❌ Не удалось отправить видео после {self.max_retries} попыток: {e}")
                    return False
            except Exception as e:
                logger.error(f"❌ Ошибка при отправке видео: {e}")
                return False
        
        return False
    
    async def send_document(self, file_path: str, caption: str = "") -> bool:
        """
        Send a document to Telegram with retry logic
        
        Args:
            file_path: Path to the document file
            caption: Optional caption for the document
            
        Returns:
            True if document was sent successfully, False otherwise
        """
        for attempt in range(self.max_retries):
            try:
                with open(file_path, 'rb') as doc_file:
                    await self.bot.send_document(
                        chat_id=self.user_id,
                        document=doc_file,
                        caption=caption
                    )
                logger.info(f"✅ Документ отправлен в Telegram")
                return True
            except (NetworkError, TimedOut) as e:
                if attempt < self.max_retries - 1:
                    logger.warning(f"⚠️ Ошибка сети при отправке документа (попытка {attempt + 1}/{self.max_retries}): {e}")
                    await asyncio.sleep(self.retry_delay)
                else:
                    logger.error(f"❌ Не удалось отправить документ после {self.max_retries} попыток: {e}")
                    return False
            except Exception as e:
                logger.error(f"❌ Ошибка при отправке документа: {e}")
                return False
        
        return False
