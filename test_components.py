import os
import asyncio
from dotenv import load_dotenv
from src.logger import logger
from src.openai_handler import OpenAIHandler
from src.telegram_handler import TelegramHandler

load_dotenv()

async def test_all():
    logger.info("🧪 Начало тестирования компонентов")
    
    # Тест 1: OpenAI
    logger.info("\n📝 Тест 1: OpenAI Handler")
    try:
        openai = OpenAIHandler()
        logger.info("✅ OpenAI Handler инициализирован")
    except Exception as e:
        logger.error(f"❌ Ошибка OpenAI: {e}")
    
    # Тест 2: Telegram
    logger.info("\n📱 Тест 2: Telegram Handler")
    try:
        telegram = TelegramHandler()
        logger.info("✅ Telegram Handler инициализирован")
    except Exception as e:
        logger.error(f"❌ Ошибка Telegram: {e}")
    
    # Тест 3: .env переменные
    logger.info("\n⚙️ Тест 3: Переменные окружения")
    required_vars = [
        'OPENAI_API_KEY',
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_USER_ID',
        'GOOGLE_DRIVE_FOLDER_ID',
        'GOOGLE_SERVICE_ACCOUNT_PATH'
    ]
    
    for var in required_vars:
        if os.getenv(var):
            logger.info(f"✅ {var} установлена")
        else:
            logger.warning(f"⚠️ {var} не установлена")
    
    logger.info("\n✅ Тестирование завершено!")

if __name__ == "__main__":
    asyncio.run(test_all())
