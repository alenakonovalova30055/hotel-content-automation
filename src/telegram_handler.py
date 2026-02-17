import os
from telegram import Bot
from telegram.error import TelegramError
from src.logger import logger

class TelegramHandler:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.user_id = os.getenv('TELEGRAM_USER_ID')
        self.bot = Bot(token=self.token)
    
    async def send_message(self, text):
        try:
            await self.bot.send_message(chat_id=self.user_id, text=text)
            logger.info(f"✅ Сообщение отправлено в Telegram")
        except TelegramError as e:
            logger.error(f"❌ Ошибка Telegram: {e}")
    
    async def send_video(self, video_path, caption=""):
        try:
            with open(video_path, 'rb') as video_file:
                await self.bot.send_video(
                    chat_id=self.user_id,
                    video=video_file,
                    caption=caption
                )
            logger.info(f"✅ Видео отправлено в Telegram")
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке видео: {e}")
    
    async def send_document(self, file_path, caption=""):
        try:
            with open(file_path, 'rb') as doc_file:
                await self.bot.send_document(
                    chat_id=self.user_id,
                    document=doc_file,
                    caption=caption
                )
            logger.info(f"✅ Документ отправлен в Telegram")
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке документа: {e}")
