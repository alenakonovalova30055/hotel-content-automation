import asyncio
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from src.logger import logger
from src.google_drive import authenticate_drive, list_all_files_recursive, download_file
from src.telegram_handler import TelegramHandler
from src.openai_handler import OpenAIHandler

load_dotenv()

def run_bot():
    """Запускает основной процесс бота"""
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"❌ Ошибка в scheduler: {e}")

async def main():
    logger.info("🤖 Запуск Bot по расписанию")
    
    try:
        # 1. Аутентификация Google Drive
        drive_service = authenticate_drive()
        folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        
        # 2. Получение списка файлов
        files = list_all_files_recursive(drive_service, folder_id)
        
        if not files:
            logger.warning("⚠️ Файлы не найдены")
            return
        
        # 3. Инициализация обработчиков
        openai_handler = OpenAIHandler()
        telegram_handler = TelegramHandler()
        
        # 4. Обработка файлов (первые 3)
        for file in files[:3]:
            file_name = file['name']
            file_id = file['id']
            
            logger.info(f"📄 Обработка файла: {file_name}")
            
            # Скачиваем файл
            file_path = download_file(drive_service, file_id, file_name)
            
            if file_path:
                # Читаем содержимое
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Генерируем описание
                description = openai_handler.generate_description(content)
                
                if description:
                    # Отправляем в Telegram
                    await telegram_handler.send_message(f"📝 {file_name}\n\n{description}")
                
                # Удаляем временный файл
                os.remove(file_path)
        
        logger.info("✅ Процесс по расписанию завершен")
    
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")

def start_scheduler():
    """Запускает scheduler"""
    scheduler = BackgroundScheduler()
    
    # Запускаем каждый день в 09:00
    scheduler.add_job(run_bot, 'cron', hour=9, minute=0, id='bot_job')
    
    scheduler.start()
    logger.info("⏰ Scheduler запущен")
    logger.info("📅 Бот будет запускаться каждый день в 09:00")
    
    return scheduler

if __name__ == "__main__":
    scheduler = start_scheduler()
    
    try:
        # Бот будет работать бесконечно
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("🛑 Scheduler остановлен")
        scheduler.shutdown()
