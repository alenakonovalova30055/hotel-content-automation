import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from src.logger import logger

SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_drive():
    try:
        creds = service_account.Credentials.from_service_account_file(
            os.getenv('GOOGLE_SERVICE_ACCOUNT_PATH'),
            scopes=SCOPES
        )
        service = build('drive', 'v3', credentials=creds)
        logger.info("✅ Google Drive аутентификация успешна")
        return service
    except Exception as e:
        logger.error(f"❌ Ошибка аутентификации Google Drive: {e}")
        raise

def list_files_in_folder(service, folder_id):
    try:
        query = f"'{folder_id}' in parents and trashed=false"
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

def download_file(service, file_id, file_name):
    try:
        request = service.files().get_media(fileId=file_id)
        file_path = f"temp/{file_name}"
        os.makedirs("temp", exist_ok=True)
        with open(file_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
        logger.info(f"✅ Файл скачан: {file_name}")
        return file_path
    except Exception as e:
        logger.error(f"❌ Ошибка при скачивании: {e}")
        return None
