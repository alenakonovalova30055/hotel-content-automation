# Usage Examples

This document provides practical examples of how to use the Hotel Content Automation system.

## 🚀 Basic Usage

### First Run

```bash
# 1. Setup (first time only)
cp .env.example .env
nano .env  # Fill in your credentials

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Run the automation
python main.py
```

### Expected Output

```
================================================================================
Starting hotel content automation workflow
================================================================================
Initializing components...
Google Drive handler initialized for folder: 1ahvhQ7r0yU_TIqC-UHdw9dRfBZAELUeV
Successfully authenticated with Google Drive
Google Docs handler initialized
OpenAI handler initialized
Text designer initialized
Video editor initialized

Selected content type: video

Loading hotel description and reference posts...
Found folder 'RAW_VIDEO' with ID: abc123
Found 15 video files

Selected video: hotel_tour.mp4
Video duration: 25.45s

Generating text overlay with OpenAI...
Generated text overlay: Твой идеальный отдых

Generating Instagram caption with OpenAI...
Generated caption: Откройте для себя комфорт в Atlas Apart ✨ Ваш дом вдали от дома 🏨

Creating video with text overlay...
Video created successfully: output/video_20240217_103045.mp4

Sending video to Telegram for approval...
✅ Video sent to Telegram successfully!
📹 Output file: output/video_20240217_103045.mp4
📝 Caption: Откройте для себя комфорт в Atlas Apart ✨

================================================================================
Workflow completed successfully!
================================================================================
```

## 📊 Common Scenarios

### Scenario 1: Generate Multiple Videos in Sequence

```bash
# Run multiple times
python main.py
python main.py
python main.py

# Each run creates a new video with:
# - Random content selection
# - Unique text generation
# - Different text position and color
```

### Scenario 2: Test Without Sending to Telegram

Edit `main.py` and comment out the Telegram sending:

```python
# Send to Telegram for approval
# logger.info("Sending video to Telegram for approval...")
# 
# telegram_success = await send_video_simple(
#     bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
#     user_id=int(os.getenv('TELEGRAM_USER_ID')),
#     video_path=str(output_video_path),
#     caption=caption
# )

logger.info(f"Video saved locally: {output_video_path}")
```

### Scenario 3: Force Video Content Only

Edit `.env`:

```env
VIDEO_PERCENTAGE=100
CAROUSEL_PERCENTAGE=0
```

### Scenario 4: Force Carousel Content Only

Edit `.env`:

```env
VIDEO_PERCENTAGE=0
CAROUSEL_PERCENTAGE=100
```

## 🔧 Customization Examples

### Change Text Colors

Edit `templates/style_guide.json`:

```json
{
  "text_colors": [
    "white",
    "#FFD700",  // Gold
    "#FF69B4",  // Hot pink
    "#87CEEB"   // Sky blue
  ]
}
```

### Change Text Positions

```json
{
  "text_positions": [
    "bottom",    // Only bottom
    "center"     // And center
  ]
}
```

### Change Font Size

```json
{
  "font_sizes": {
    "small": 50,
    "medium": 80,
    "large": 120
  }
}
```

### Change Video Duration Limits

Edit `.env`:

```env
MIN_VIDEO_DURATION=15
MAX_VIDEO_DURATION=20
```

## 🧪 Testing Examples

### Test Google Drive Connection

```python
from src.google_drive import GoogleDriveHandler
from dotenv import load_dotenv
import os

load_dotenv()

handler = GoogleDriveHandler(
    service_account_file=os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE'),
    folder_id=os.getenv('GOOGLE_DRIVE_FOLDER_ID')
)

# List videos
videos = handler.get_video_files()
print(f"Found {len(videos)} videos:")
for v in videos:
    print(f"  - {v['name']}")

# List photos
photos = handler.get_photo_files()
print(f"Found {len(photos)} photos:")
for p in photos:
    print(f"  - {p['name']}")
```

### Test OpenAI Text Generation

```python
from src.openai_handler import OpenAIHandler
from dotenv import load_dotenv
import os

load_dotenv()

handler = OpenAIHandler(api_key=os.getenv('OPENAI_API_KEY'))

hotel_desc = "Atlas Apart - комфортные апартаменты в центре города"
references = [
    "Утро в Atlas Apart ☀️",
    "Ваш идеальный отдых 🏨",
    "Комфорт и стиль 💫"
]

# Generate caption
caption = handler.generate_caption(hotel_desc, references, "video")
print(f"Caption: {caption}")

# Generate text overlay
overlay = handler.generate_short_text_overlay(hotel_desc, references)
print(f"Overlay: {overlay}")
```

### Test Video Creation

```python
from src.video_editor import VideoEditor
from src.text_designer import TextDesigner

designer = TextDesigner()
editor = VideoEditor(text_designer=designer)

# Create video with text
editor.create_video_with_text(
    video_path="test_video.mp4",
    text="Твой идеальный отдых",
    output_path="output/test_output.mp4",
    max_duration=15.0
)
```

### Test Telegram Bot

```python
import asyncio
from src.telegram_bot import send_video_simple
from dotenv import load_dotenv
import os

load_dotenv()

async def test_telegram():
    await send_video_simple(
        bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
        user_id=int(os.getenv('TELEGRAM_USER_ID')),
        video_path="output/test_video.mp4",
        caption="Test video from automation system"
    )

asyncio.run(test_telegram())
```

## 📝 Logging Examples

### View Logs in Real-Time

```bash
# Terminal 1: Run the script
python main.py

# Terminal 2: Watch logs
tail -f logs/process_*.log
```

### Filter Logs by Level

```bash
# Show only errors
grep "ERROR" logs/process_*.log

# Show only warnings and errors
grep -E "WARNING|ERROR" logs/process_*.log

# Show OpenAI related logs
grep "OpenAI" logs/process_*.log
```

### Custom Log Analysis

```python
import re
from datetime import datetime

# Parse log file
with open('logs/process_20240217_103045.log', 'r') as f:
    for line in f:
        if 'Generated caption' in line:
            print(line.strip())
```

## 🔄 Automation Examples

### Run Every Hour (Linux/Mac - Cron)

```bash
# Edit crontab
crontab -e

# Add this line (run every hour at :00)
0 * * * * cd /path/to/hotel-content-automation && /path/to/venv/bin/python main.py >> logs/cron.log 2>&1
```

### Run Every Day at 10 AM (Linux/Mac - Cron)

```bash
0 10 * * * cd /path/to/hotel-content-automation && /path/to/venv/bin/python main.py
```

### Run on System Startup (Linux - Systemd)

Create `/etc/systemd/system/hotel-automation.service`:

```ini
[Unit]
Description=Hotel Content Automation
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/hotel-content-automation
ExecStart=/path/to/venv/bin/python main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable hotel-automation
sudo systemctl start hotel-automation
sudo systemctl status hotel-automation
```

### Run Every Day at 10 AM (Windows - Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Hotel Content Automation"
4. Trigger: Daily at 10:00 AM
5. Action: Start a program
6. Program: `C:\path\to\venv\Scripts\python.exe`
7. Arguments: `main.py`
8. Start in: `C:\path\to\hotel-content-automation`

## 🐛 Debugging Examples

### Enable Debug Logging

Edit `src/logger.py`:

```python
# Change INFO to DEBUG
logger.setLevel(logging.DEBUG)
console_handler.setLevel(logging.DEBUG)
```

### Test Individual Components

```python
# Test just the text designer
from src.text_designer import TextDesigner

designer = TextDesigner()
config = designer.create_text_clip_config(
    text="Test text",
    video_width=1920,
    video_height=1080,
    duration=10.0
)
print(config)
```

### Check API Connectivity

```python
# Test Google Drive API
try:
    from src.google_drive import GoogleDriveHandler
    handler = GoogleDriveHandler('service-account.json', 'folder_id')
    print("✅ Google Drive: Connected")
except Exception as e:
    print(f"❌ Google Drive: {e}")

# Test OpenAI API
try:
    from src.openai_handler import OpenAIHandler
    handler = OpenAIHandler('api_key')
    print("✅ OpenAI: Connected")
except Exception as e:
    print(f"❌ OpenAI: {e}")
```

## 📊 Performance Examples

### Measure Execution Time

```python
import time

start_time = time.time()

# Run automation
asyncio.run(process_content())

end_time = time.time()
print(f"Total time: {end_time - start_time:.2f} seconds")
```

### Profile Memory Usage

```python
import tracemalloc

tracemalloc.start()

# Run automation
asyncio.run(process_content())

current, peak = tracemalloc.get_traced_memory()
print(f"Current memory: {current / 1024 / 1024:.2f} MB")
print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")
tracemalloc.stop()
```

## 🎨 Style Examples

### Minimal Style (Clean, Simple)

`templates/style_guide.json`:
```json
{
  "text_colors": ["white"],
  "text_positions": ["bottom"],
  "font_sizes": {"medium": 50}
}
```

### Bold Style (Large, Colorful)

```json
{
  "text_colors": ["#FFD700", "#FF1493", "#00FF00"],
  "text_positions": ["center"],
  "font_sizes": {"medium": 100}
}
```

### Random Style (Varied, Dynamic)

```json
{
  "text_colors": ["white", "#FFE5B4", "#FFB6C1", "#ADD8E6", "#F0E68C"],
  "text_positions": ["bottom", "center", "top-left", "top-right", "bottom-left", "bottom-right"],
  "font_sizes": {"medium": 60}
}
```

## 📱 Telegram Examples

### Custom Approval Message

Edit `src/telegram_bot.py`, modify the message in `send_video_simple`:

```python
message = f"🎬 Новый контент для Atlas Apart\n\n"
message += f"📝 {caption}\n\n"
message += f"⏱️ Длительность: {duration}с\n"
message += f"📅 Создано: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
message += "Выберите действие:"
```

### Send to Multiple Users

```python
user_ids = [220317440, 987654321, 123456789]

for user_id in user_ids:
    await send_video_simple(bot_token, user_id, video_path, caption)
```

## 🎯 Production Examples

### Production Configuration

`.env`:
```env
# Use production API keys
OPENAI_API_KEY=sk-prod-...

# Enable error notifications
TELEGRAM_ERROR_NOTIFICATIONS=true

# Use high quality settings
VIDEO_QUALITY=high
```

### Error Handling

```python
import sys
from src.logger import get_logger

logger = get_logger()

try:
    asyncio.run(process_content())
except Exception as e:
    logger.error(f"Critical error: {e}", exc_info=True)
    # Send error notification
    # Cleanup resources
    sys.exit(1)
```

## 📚 More Examples

For more examples and use cases, see:
- `README.md` - General usage
- `setup.md` - Setup examples
- `ARCHITECTURE.md` - Technical details
- `test_structure.py` - Testing examples

---

**Last Updated**: 2026-02-17
