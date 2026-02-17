"""Main orchestration script for hotel content automation."""

import os
import sys
import random
import asyncio
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from src.logger import setup_logger
from src.google_drive import GoogleDriveHandler
from src.google_docs import GoogleDocsHandler
from src.openai_handler import OpenAIHandler
from src.text_designer import TextDesigner
from src.video_editor import VideoEditor
from src.telegram_bot import send_video_simple

# Load environment variables
load_dotenv()

# Setup logger
logger = setup_logger()


def validate_environment():
    """Validate that all required environment variables are set."""
    required_vars = [
        'OPENAI_API_KEY',
        'GOOGLE_DRIVE_FOLDER_ID',
        'GOOGLE_SERVICE_ACCOUNT_FILE',
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_USER_ID'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please copy .env.example to .env and fill in the values")
        return False
    
    return True


def select_content_type():
    """
    Select content type based on percentage distribution.
    
    Returns:
        'video' or 'carousel'
    """
    video_percentage = int(os.getenv('VIDEO_PERCENTAGE', '70'))
    return 'video' if random.randint(1, 100) <= video_percentage else 'carousel'


async def process_content():
    """Main content processing workflow."""
    try:
        logger.info("="*80)
        logger.info("Starting hotel content automation workflow")
        logger.info("="*80)
        
        # Validate environment
        if not validate_environment():
            return False
        
        # Initialize components
        logger.info("Initializing components...")
        
        drive_handler = GoogleDriveHandler(
            service_account_file=os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE'),
            folder_id=os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        )
        
        docs_handler = GoogleDocsHandler(
            service_account_file=os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE')
        )
        
        openai_handler = OpenAIHandler(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        text_designer = TextDesigner()
        video_editor = VideoEditor(text_designer=text_designer)
        
        # Select content type
        content_type = select_content_type()
        logger.info(f"Selected content type: {content_type}")
        
        # Get hotel description and reference posts
        logger.info("Loading hotel description and reference posts...")
        
        # Try to read hotel description
        hotel_description = "Atlas Apart - ваш идеальный отдых в центре города. Комфортные апартаменты с современным дизайном."
        text_files = drive_handler.get_text_files(os.getenv('TEXTS_FOLDER', 'TEXTS'))
        if text_files:
            # Download first text file
            text_file = text_files[0]
            temp_text_path = f"/tmp/hotel_description_{text_file['id']}.txt"
            if drive_handler.download_file(text_file['id'], temp_text_path):
                hotel_desc = docs_handler.read_text_file(temp_text_path)
                if hotel_desc:
                    hotel_description = hotel_desc
        
        logger.info(f"Hotel description loaded: {hotel_description[:100]}...")
        
        # Load reference posts
        reference_posts = []
        ref_files = drive_handler.get_reference_posts(os.getenv('POSTS_REFERENCE_FOLDER', 'POSTS_REFERENCE'))
        if ref_files:
            for ref_file in ref_files[:5]:  # Get up to 5 reference posts
                temp_ref_path = f"/tmp/reference_{ref_file['id']}.txt"
                if drive_handler.download_file(ref_file['id'], temp_ref_path):
                    ref_text = docs_handler.read_text_file(temp_ref_path)
                    if ref_text:
                        reference_posts.append(ref_text)
        
        # If no reference posts found, use defaults
        if not reference_posts:
            reference_posts = [
                "Утро в Atlas Apart ☀️ Начните свой день с комфорта и уюта",
                "Идеальное место для вашего отпуска 🏨 Современные апартаменты в центре города",
                "Atlas Apart - где каждый день как отпуск 🌟 Бронируйте сейчас!",
                "Ваш дом вдали от дома 🏡 Комфорт и стиль в каждой детали",
                "Незабываемый отдых начинается здесь 💫 Atlas Apart"
            ]
        
        logger.info(f"Loaded {len(reference_posts)} reference posts")
        
        # Create output directory
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        # Generate content based on type
        if content_type == 'video':
            logger.info("Processing video content...")
            
            # Get video files
            videos = drive_handler.get_video_files(os.getenv('RAW_VIDEO_FOLDER', 'RAW_VIDEO'))
            if not videos:
                logger.error("No video files found in RAW_VIDEO folder")
                return False
            
            # Select random video
            selected_video = random.choice(videos)
            logger.info(f"Selected video: {selected_video['name']}")
            
            # Download video
            temp_video_path = f"/tmp/input_video_{selected_video['id']}.mp4"
            if not drive_handler.download_file(selected_video['id'], temp_video_path):
                logger.error("Failed to download video")
                return False
            
            # Get video duration
            duration = video_editor.get_video_duration(temp_video_path)
            if duration:
                logger.info(f"Video duration: {duration:.2f}s")
            
            # Generate text overlay
            logger.info("Generating text overlay with OpenAI...")
            text_overlay = openai_handler.generate_short_text_overlay(
                hotel_description=hotel_description,
                reference_posts=reference_posts
            )
            
            if not text_overlay:
                logger.warning("Failed to generate text overlay, using default")
                text_overlay = "Твой идеальный отдых"
            
            logger.info(f"Generated text overlay: {text_overlay}")
            
            # Generate Instagram caption
            logger.info("Generating Instagram caption with OpenAI...")
            caption = openai_handler.generate_caption(
                hotel_description=hotel_description,
                reference_posts=reference_posts,
                content_type='video'
            )
            
            if not caption:
                logger.warning("Failed to generate caption, using default")
                caption = "Ваш комфортный отдых в Atlas Apart ✨"
            
            logger.info(f"Generated caption: {caption}")
            
            # Create video with text
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_video_path = output_dir / f"video_{timestamp}.mp4"
            
            logger.info("Creating video with text overlay...")
            success = video_editor.create_video_with_text(
                video_path=temp_video_path,
                text=text_overlay,
                output_path=str(output_video_path),
                max_duration=float(os.getenv('MAX_VIDEO_DURATION', '30'))
            )
            
            if not success:
                logger.error("Failed to create video with text")
                return False
            
            logger.info(f"Video created successfully: {output_video_path}")
        
        else:  # carousel
            logger.info("Processing carousel content...")
            
            # Get photo files
            photos = drive_handler.get_photo_files(os.getenv('RAW_PHOTO_FOLDER', 'RAW_PHOTO'))
            if not photos:
                logger.error("No photo files found in RAW_PHOTO folder")
                return False
            
            # Select random photos (3-5 photos)
            num_photos = random.randint(3, min(5, len(photos)))
            selected_photos = random.sample(photos, num_photos)
            logger.info(f"Selected {num_photos} photos for carousel")
            
            # Download photos
            temp_photo_paths = []
            for photo in selected_photos:
                temp_path = f"/tmp/photo_{photo['id']}.jpg"
                if drive_handler.download_file(photo['id'], temp_path):
                    temp_photo_paths.append(temp_path)
            
            if not temp_photo_paths:
                logger.error("Failed to download photos")
                return False
            
            # Generate text overlay
            logger.info("Generating text overlay with OpenAI...")
            text_overlay = openai_handler.generate_short_text_overlay(
                hotel_description=hotel_description,
                reference_posts=reference_posts
            )
            
            if not text_overlay:
                text_overlay = "Atlas Apart - твой выбор"
            
            # Generate Instagram caption
            logger.info("Generating Instagram caption with OpenAI...")
            caption = openai_handler.generate_caption(
                hotel_description=hotel_description,
                reference_posts=reference_posts,
                content_type='carousel'
            )
            
            if not caption:
                caption = "Откройте для себя Atlas Apart 🏨✨"
            
            # Create carousel video
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_video_path = output_dir / f"carousel_{timestamp}.mp4"
            
            logger.info("Creating carousel video...")
            success = video_editor.create_carousel_video(
                image_paths=temp_photo_paths,
                text=text_overlay,
                output_path=str(output_video_path),
                duration_per_image=3.0,
                total_duration=15.0
            )
            
            if not success:
                logger.error("Failed to create carousel video")
                return False
            
            logger.info(f"Carousel video created successfully: {output_video_path}")
        
        # Send to Telegram for approval
        logger.info("Sending video to Telegram for approval...")
        
        telegram_success = await send_video_simple(
            bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
            user_id=int(os.getenv('TELEGRAM_USER_ID')),
            video_path=str(output_video_path),
            caption=caption
        )
        
        if telegram_success:
            logger.info("✅ Video sent to Telegram successfully!")
            logger.info(f"📹 Output file: {output_video_path}")
            logger.info(f"📝 Caption: {caption}")
        else:
            logger.warning("Failed to send video to Telegram, but video was created successfully")
            logger.info(f"Video saved locally: {output_video_path}")
        
        logger.info("="*80)
        logger.info("Workflow completed successfully!")
        logger.info("="*80)
        
        return True
    
    except Exception as e:
        logger.error(f"Error in main workflow: {e}", exc_info=True)
        return False


def main():
    """Entry point for the application."""
    try:
        # Run async workflow
        success = asyncio.run(process_content())
        
        if success:
            logger.info("✅ All operations completed successfully!")
            sys.exit(0)
        else:
            logger.error("❌ Workflow failed. Check logs for details.")
            sys.exit(1)
    
    except KeyboardInterrupt:
        logger.info("Workflow interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
