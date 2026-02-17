# 🏨 Hotel Content Automation

Автоматизация создания контента для отелей с использованием Google Drive, OpenAI и Telegram.

## 🚀 Возможности

- 📄 Работа с Google Drive (загрузка, скачивание, преобразование документов)
- 🤖 Интеграция с OpenAI для генерации и редактирования текстов
- 📱 Отправка уведомлений через Telegram
- 📊 Логирование всех операций
- ⚙️ Асинхронная обработка

## 📋 Требования

- Python 3.9+
- Google Service Account (для Google Drive)
- OpenAI API Key
- Telegram Bot Token

## 🔧 Установка

### 1. Клонируем репозиторий
\`\`\`bash
git clone https://github.com/alenakonovalova30055/hotel-content-automation.git
cd hotel-content-automation
\`\`\`

### 2. Создаем виртуальное окружение
\`\`\`bash
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\\Scripts\\activate
\`\`\`

### 3. Устанавливаем зависимости
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Настраиваем переменные окружения
\`\`\`bash
cp .env.example .env
# Отредактируйте .env и добавьте реальные значения
nano .env
\`\`\`

### 5. Добавляем Google Service Account
\`\`\`bash
# Поместите google-service-account.json в папку secrets/
cp /path/to/google-service-account.json secrets/
\`\`\`

## 📦 Структура проекта

\`\`\`
hotel-content-automation/
├── src/
│   ├── __init__.py
│   ├── logger.py           # 📝 Логирование
│   ├── google_drive.py     # 🔵 Google Drive интеграция
│   ├── openai_handler.py   # 🤖 OpenAI интеграция
│   └── telegram_handler.py # 📱 Telegram интеграция
├── secrets/
│   └── google-service-account.json
├── logs/
├── config.py               # ⚙️ Конфигурация
├─��� main.py                 # 🚀 Главная программа
├── requirements.txt        # 📚 Зависимости
├── .env.example            # 📋 Пример переменных окружения
└── README.md               # 📖 Этот файл
\`\`\`

## 🔑 Переменные окружения

\`\`\`env
# OpenAI
OPENAI_API_KEY=sk-xxxxx

# Telegram
TELEGRAM_BOT_TOKEN=xxxxx
TELEGRAM_USER_ID=xxxxx

# Google Drive
GOOGLE_DRIVE_FOLDER_ID=xxxxx
GOOGLE_SERVICE_ACCOUNT_PATH=secrets/google-service-account.json
\`\`\`

## 🚀 Использование

### Запуск основной программы
\`\`\`bash
python3 main.py
\`\`\`

### Тестирование компонентов
\`\`\`bash
python3 test_components.py
\`\`\`

## 📚 API

### Logger
\`\`\`python
from src.logger import logger

logger.info("Сообщение")
logger.error("Ошибка")
logger.warning("Предупреждение")
\`\`\`

### Google Drive
\`\`\`python
from src.google_drive import authenticate_drive, upload_file

service = authenticate_drive()
file_

cat > README.md << 'READMEEOF'
# 🏨 Hotel Content Automation

Автоматизация создания контента для отелей с использованием Google Drive, OpenAI и Telegram.

## 🚀 Возможности

- 📄 Работа с Google Drive (загрузка, скачивание, преобразование документов)
- 🤖 Интеграция с OpenAI для генерации и редактирования текстов
- 📱 Отправка уведомлений через Telegram
- 📊 Логирование всех операций
- ⚙️ Асинхронная обработка

## 📋 Требования

- Python 3.9+
- Google Service Account (для Google Drive)
- OpenAI API Key
- Telegram Bot Token

## 🔧 Установка

### 1. Клонируем репозиторий
\`\`\`bash
git clone https://github.com/alenakonovalova30055/hotel-content-automation.git
cd hotel-content-automation
\`\`\`

### 2. Создаем виртуальное окружение
\`\`\`bash
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\\Scripts\\activate
\`\`\`

### 3. Устанавливаем зависимости
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Настраиваем переменные окружения
\`\`\`bash
cp .env.example .env
# Отредактируйте .env и добавьте реальные значения
nano .env
\`\`\`

### 5. Добавляем Google Service Account
\`\`\`bash
# Поместите google-service-account.json в папку secrets/
cp /path/to/google-service-account.json secrets/
\`\`\`

## 📦 Структура проекта

\`\`\`
hotel-content-automation/
├── src/
│   ├── __init__.py
│   ├── logger.py           # 📝 Логирование
│   ├── google_drive.py     # 🔵 Google Drive интеграция
│   ├── openai_handler.py   # 🤖 OpenAI интеграция
│   └── telegram_handler.py # 📱 Telegram интеграция
├── secrets/
│   └── google-service-account.json
├── logs/
├── config.py               # ⚙️ Конфигурация
├─��� main.py                 # 🚀 Главная программа
├── requirements.txt        # 📚 Зависимости
├── .env.example            # 📋 Пример переменных окружения
└── README.md               # 📖 Этот файл
\`\`\`

## 🔑 Переменные окружения

\`\`\`env
# OpenAI
OPENAI_API_KEY=sk-xxxxx

# Telegram
TELEGRAM_BOT_TOKEN=xxxxx
TELEGRAM_USER_ID=xxxxx

# Google Drive
GOOGLE_DRIVE_FOLDER_ID=xxxxx
GOOGLE_SERVICE_ACCOUNT_PATH=secrets/google-service-account.json
\`\`\`

## 🚀 Использование

### Запуск основной программы
\`\`\`bash
python3 main.py
\`\`\`

### Тестирование компонентов
\`\`\`bash
python3 test_components.py
\`\`\`

## 📚 API

### Logger
\`\`\`python
from src.logger import logger

logger.info("Сообщение")
logger.error("Ошибка")
logger.warning("Предупреждение")
\`\`\`

### Google Drive
\`\`\`python
from src.google_drive import authenticate_drive, upload_file

service = authenticate_drive()
file_id = upload_file(service, "file.txt", folder_id)
\`\`\`

### OpenAI
\`\`\`python
from src.openai_handler import OpenAIHandler

openai = OpenAIHandler()
response = await openai.generate_text("Напишите описание отеля")
\`\`\`

### Telegram
\`\`\`python
from src.telegram_handler import TelegramHandler

telegram = TelegramHandler()
await telegram.send_message("Привет!")
\`\`\`

## 🐛 Логирование

Логи сохраняются в папке `logs/` с префиксом `process_YYYYMMDD_HHMMSS.log`

## 🔐 Безопасность

- ✅ Все секреты хранятся в `.env` (не загружаются на GitHub)
- ✅ Google Service Account в папке `secrets/`
- ✅ Все операции логируются

## 📝 Лицензия

MIT License

## 👤 Автор

alenakonovalova30055

## 📞 Контакты

- GitHub: [@alenakonovalova30055](https://github.com/alenakonovalova30055)
- Telegram: Используйте бота для связи

---

**Последнее обновление:** 2026-02-17
