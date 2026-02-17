import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from src.logger import logger

SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_drive():
    try:
        import json

service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
service_account_info = json.loads(service_account_json)

creds = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=SCOPES
)
        service = build('drive', 'v3', credentials=creds)
        logger.info("✅ Google Drive аутентификация успешна")
        return service
    except Exception as e:
        logger.error(f"❌ Ошибка аутентификации Google Drive: {e}")
        raise

def list_files_in_folder(service, folder_id):
    """Получает все файлы в папке (не включая подпапки)"""
    try:
        query = f"'{folder_id}' in parents and trashed=false and mimeType != 'application/vnd.google-apps.folder'"
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, mimeType)',
            pageSize=100
        ).execute()
        files = results.get('files', [])
        logger.info(f"📂 Найдено {len(files)} файлов")
        return files
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        return []

def list_all_files_recursive(service, folder_id):
    """Получает все файлы рекурсивно из всех подпапок"""
    all_files = []
    try:
        # Сначала получаем все файлы в текущей папке
        query = f"'{folder_id}' in parents and trashed=false"
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, mimeType)',
            pageSize=100
        ).execute()
        items = results.get('files', [])
        
        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                # Если это папка, ищем файлы внутри неё
                logger.info(f"📂 Ищу файлы в папке: {item['name']}")
                sub_files = list_all_files_recursive(service, item['id'])
                all_files.extend(sub_files)
            else:
                # Если это файл, добавляем в список
                all_files.append(item)
        
        return all_files
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        return []

def download_file(service, file_id, file_name):
    """Скачивает файл с Google Drive, поддерживает Google Docs"""
    try:
        # Получаем информацию о файле
        file_info = service.files().get(fileId=file_id, fields='mimeType').execute()
        mime_type = file_info.get('mimeType')
        
        os.makedirs("temp", exist_ok=True)
        
        # Если это Google Docs
        if mime_type == 'application/vnd.google-apps.document':
            logger.info(f"📄 Экспортирую Google Docs: {file_name}")
            request = service.files().export_media(fileId=file_id, mimeType='text/plain')
            file_path = f"temp/{file_name}.txt"
            content = request.execute()
            with open(file_path, 'wb') as f:
                f.write(content)
            logger.info(f"✅ Google Docs экспортирован: {file_name}")
            return file_path
        
        # Если это Google Sheets
        elif mime_type == 'application/vnd.google-apps.spreadsheet':
            logger.info(f"📊 Экспортирую Google Sheets: {file_name}")
            request = service.files().export_media(fileId=file_id, mimeType='text/csv')
            file_path = f"temp/{file_name}.csv"
            content = request.execute()
            with open(file_path, 'wb') as f:
                f.write(content)
            logger.info(f"✅ Google Sheets экспортирован: {file_name}")
            return file_path
        
        # Для обычных файлов
        else:
            logger.info(f"📥 Скачиваю файл: {file_name}")
            request = service.files().get_media(fileId=file_id)
            file_path = f"temp/{file_name}"
            content = request.execute()
            with open(file_path, 'wb') as f:
                f.write(content)
            logger.info(f"✅ Файл скачан: {file_name}")
            return file_path
            
    except Exception as e:
        logger.error(f"❌ Ошибка при скачивании: {e}")
        return None
