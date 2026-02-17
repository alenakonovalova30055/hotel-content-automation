import os
from dotenv import load_dotenv

load_dotenv()

# Google Drive
GOOGLE_DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID')

# OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = "gpt-4-turbo"

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_USER_ID = os.getenv('TELEGRAM_USER_ID')

# Параметры обработки видео
VIDEO_RESOLUTION = (1920, 1080)
VIDEO_FPS = 30
VIDEO_BITRATE = "5000k"

# Параметры обработки изображений
IMAGE_QUALITY = 95
MAX_IMAGE_SIZE = (2560, 2560)

# Пути
TEMP_DIR = "temp"
LOGS_DIR = "logs"
OUTPUT_DIR = "output"

# Создаем необходимые папки
for directory in [TEMP_DIR, LOGS_DIR, OUTPUT_DIR]:
    os.makedirs(directory, exist_ok=True)
