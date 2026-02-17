import asyncio
import os
from dotenv import load_dotenv
from src.telegram_handler import TelegramHandler
from src.openai_handler import OpenAIHandler

# Загружаем переменные окружения
load_dotenv()

async def test():
    print(f"✅ Токен загружен: {os.getenv('TELEGRAM_BOT_TOKEN')[:20]}...")
    
    # Инициализируем обработчики
    telegram = TelegramHandler()
    openai = OpenAIHandler()
    
    # Генерируем описание
    description = openai.generate_description("Тестовый документ про отель")
    
    # Отправляем в Telegram
    await telegram.send_message(f"🤖 Тестовое сообщение\n\n{description}")
    print("✅ Сообщение ��тправлено в Telegram!")

if __name__ == "__main__":
    asyncio.run(test())
