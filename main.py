import os
import asyncio
from dotenv import load_dotenv
from src.logger import logger
from src.google_drive import authenticate_drive, list_all_files_recursive, download_file
from src.telegram_handler import TelegramHandler
from src.openai_handler import OpenAIHandler
from src.content_processor import ContentProcessor

load_dotenv()

async def main():
    logger.info("🚀 Запуск Hotel Content Automation Bot")
    
    try:
        # 1. Аутентификация Google Drive
        logger.info("📁 Подключение к Google Drive...")
        drive_service = authenticate_drive()
        
        folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        
        # 2. Получение списка файлов (рекурсивно из подпапок)
        logger.info("📂 Получение списка файлов...")
        files = list_all_files_recursive(drive_service, folder_id)
        
        if not files:
            logger.warning("⚠️ Файлы не найдены")
            return
        
        # 3. Инициализация OpenAI, Telegram и Content Processor
        openai_handler = OpenAIHandler()
        telegram_handler = TelegramHandler()
        content_processor = ContentProcessor()
        
        # 4. Обработка файлов
        for file in files[:3]:  # Обрабатываем первые 3 файла
            file_name = file['name']
            file_id = file['id']
            
            logger.info(f"📄 Обработка файла: {file_name}")
            
            # Скачиваем файл
            file_path = download_file(drive_service, file_id, file_name)
            
            if file_path:
                # Обрабатываем содержимое файла с помощью ContentProcessor
                content = content_processor.process_file(file_path)
                
                if content:
                    # Генерируем описание с помощью OpenAI
                    description = openai_handler.generate_description(content)
                    
                    if description:
                        # Отправляем в Telegram
                        await telegram_handler.send_message(f"📝 {file_name}\n\n{description}")
                else:
                    logger.warning(f"⚠️ Не удалось извлечь контент из файла: {file_name}")
                
                # Удаляем временный файл
                os.remove(file_path)
        
        logger.info("✅ Процесс завершен успешно")
    
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
