import asyncio
import os
from dotenv import load_dotenv
from src.logger import logger
from src.google_drive import authenticate_drive, list_all_files_recursive, download_file
from src.telegram_handler import TelegramHandler
from src.openai_handler import OpenAIHandler

load_dotenv()

async def main():
    logger.info("🚀 Запуск Bot СЕЙЧАС (тестирование)")
    
    try:
        # 1. Аутентификация Google Drive
        drive_service = authenticate_drive()
        folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        
        # 2. Получение списка файлов
        files = list_all_files_recursive(drive_service, folder_id)
        
        if not files:
            logger.warning("⚠️ Файлы не найдены")
            return
        
        logger.info(f"📂 Найдено {len(files)} файлов")
        
        # 3. Инициализация обра��отчиков
        openai_handler = OpenAIHandler()
        telegram_handler = TelegramHandler()
        
        # 4. Обработка файлов (первые 3)
        processed = 0
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
                    processed += 1
                
                # Удаляем временный файл
                os.remove(file_path)
        
        logger.info(f"✅ Обработано {processed} файлов")
    
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
