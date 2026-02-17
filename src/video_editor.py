"""Video editing functionality using MoviePy."""

import os
import random
from typing import List, Optional, Tuple
from pathlib import Path

from moviepy.editor import (
    VideoFileClip,
    ImageClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
    AudioFileClip
)
from moviepy.video.fx.all import fadein, fadeout, crossfadein, crossfadeout

from .text_designer import TextDesigner
from .logger import get_logger

logger = get_logger()


class VideoEditor:
    """Handle video editing operations."""
    
    def __init__(self, text_designer: TextDesigner = None):
        """
        Initialize video editor.
        
        Args:
            text_designer: TextDesigner instance for styling
        """
        self.text_designer = text_designer or TextDesigner()
        logger.info("Video editor initialized")
    
    def create_video_with_text(
        self,
        video_path: str,
        text: str,
        output_path: str,
        target_duration: Optional[float] = None,
        max_duration: float = 30.0
    ) -> bool:
        """
        Create video with text overlay.
        
        Args:
            video_path: Path to input video file
            text: Text to overlay on video
            output_path: Path to save output video
            target_duration: Target duration in seconds (optional)
            max_duration: Maximum allowed duration
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Processing video: {video_path}")
            
            # Load video
            video = VideoFileClip(video_path)
            original_duration = video.duration
            
            # Adjust duration if needed
            if target_duration and target_duration < original_duration:
                # Cut video to target duration from the beginning
                video = video.subclip(0, target_duration)
                logger.info(f"Video trimmed from {original_duration}s to {target_duration}s")
            elif original_duration > max_duration:
                # Trim to max duration
                video = video.subclip(0, max_duration)
                logger.info(f"Video trimmed to maximum duration: {max_duration}s")
            
            duration = video.duration
            
            # Apply fade effects
            video = fadein(video, 0.5)
            video = fadeout(video, 0.5)
            
            # Create text overlay
            text_config = self.text_designer.create_text_clip_config(
                text=text,
                video_width=video.w,
                video_height=video.h,
                duration=duration
            )
            
            # Wrap text to fit video width
            wrapped_text = self.text_designer.wrap_text(
                text,
                max_width=int(video.w * 0.8),  # 80% of video width
                font_size=text_config['font_size']
            )
            
            # Create text clip
            try:
                txt_clip = TextClip(
                    wrapped_text,
                    fontsize=text_config['font_size'],
                    color=text_config['color'],
                    stroke_color=text_config['stroke_color'],
                    stroke_width=text_config['stroke_width'],
                    method='caption',
                    size=(int(video.w * 0.8), None),
                    font='Arial'  # Using Arial as default fallback font
                )
            except Exception as e:
                logger.warning(f"Error creating text with caption method: {e}. Trying label method.")
                # Fallback to label method
                txt_clip = TextClip(
                    wrapped_text,
                    fontsize=text_config['font_size'],
                    color=text_config['color'],
                    stroke_color=text_config['stroke_color'],
                    stroke_width=text_config['stroke_width'],
                    method='label',
                    font='Arial'
                )
            
            # Set duration and position
            txt_clip = txt_clip.set_duration(duration)
            
            # Calculate position
            if text_config['position'] == 'center':
                txt_clip = txt_clip.set_position('center')
            elif text_config['position'] == 'bottom':
                txt_clip = txt_clip.set_position(('center', video.h - txt_clip.h - 50))
            elif text_config['position'] == 'top':
                txt_clip = txt_clip.set_position(('center', 50))
            elif text_config['position'] == 'top-left':
                txt_clip = txt_clip.set_position((50, 50))
            elif text_config['position'] == 'top-right':
                txt_clip = txt_clip.set_position((video.w - txt_clip.w - 50, 50))
            elif text_config['position'] == 'bottom-left':
                txt_clip = txt_clip.set_position((50, video.h - txt_clip.h - 50))
            elif text_config['position'] == 'bottom-right':
                txt_clip = txt_clip.set_position((video.w - txt_clip.w - 50, video.h - txt_clip.h - 50))
            else:
                txt_clip = txt_clip.set_position(('center', video.h - txt_clip.h - 50))
            
            # Apply fade to text
            txt_clip = fadein(txt_clip, 0.5)
            txt_clip = fadeout(txt_clip, 0.5)
            
            # Composite video with text
            final_video = CompositeVideoClip([video, txt_clip])
            
            # Create output directory if it doesn't exist
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Write output
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                fps=video.fps,
                preset='medium',
                threads=4,
                logger=None  # Suppress moviepy logging
            )
            
            # Clean up
            video.close()
            txt_clip.close()
            final_video.close()
            
            logger.info(f"Video saved successfully to: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error creating video with text: {e}")
            return False
    
    def create_carousel_video(
        self,
        image_paths: List[str],
        text: str,
        output_path: str,
        duration_per_image: float = 3.0,
        total_duration: float = 15.0
    ) -> bool:
        """
        Create video from image carousel with text overlay.
        
        Args:
            image_paths: List of image file paths
            text: Text to overlay
            output_path: Path to save output video
            duration_per_image: Duration to show each image
            total_duration: Total video duration
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Creating carousel video from {len(image_paths)} images")
            
            if not image_paths:
                logger.error("No images provided for carousel")
                return False
            
            # Calculate number of images needed
            num_images = min(len(image_paths), int(total_duration / duration_per_image))
            selected_images = random.sample(image_paths, num_images)
            
            # Create image clips
            clips = []
            for img_path in selected_images:
                img_clip = ImageClip(img_path, duration=duration_per_image)
                # Apply transitions
                img_clip = fadein(img_clip, 0.5)
                img_clip = fadeout(img_clip, 0.5)
                clips.append(img_clip)
            
            # Concatenate clips with crossfade
            if len(clips) > 1:
                video = concatenate_videoclips(clips, method="compose")
            else:
                video = clips[0]
            
            # Resize to standard Instagram size (1080x1920 for reels)
            video = video.resize(height=1920)
            if video.w > 1080:
                video = video.resize(width=1080)
            
            # Create text overlay
            text_config = self.text_designer.create_text_clip_config(
                text=text,
                video_width=video.w,
                video_height=video.h,
                duration=video.duration
            )
            
            wrapped_text = self.text_designer.wrap_text(
                text,
                max_width=int(video.w * 0.8),
                font_size=text_config['font_size']
            )
            
            # Create text clip
            try:
                txt_clip = TextClip(
                    wrapped_text,
                    fontsize=text_config['font_size'],
                    color=text_config['color'],
                    stroke_color=text_config['stroke_color'],
                    stroke_width=text_config['stroke_width'],
                    method='caption',
                    size=(int(video.w * 0.8), None),
                    font='Arial'
                )
            except:
                txt_clip = TextClip(
                    wrapped_text,
                    fontsize=text_config['font_size'],
                    color=text_config['color'],
                    stroke_color=text_config['stroke_color'],
                    stroke_width=text_config['stroke_width'],
                    method='label',
                    font='Arial'
                )
            
            txt_clip = txt_clip.set_duration(video.duration)
            txt_clip = txt_clip.set_position(('center', video.h - txt_clip.h - 50))
            txt_clip = fadein(txt_clip, 0.5)
            txt_clip = fadeout(txt_clip, 0.5)
            
            # Composite video
            final_video = CompositeVideoClip([video, txt_clip])
            
            # Create output directory
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Write output
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                fps=24,
                preset='medium',
                threads=4,
                logger=None
            )
            
            # Clean up
            for clip in clips:
                clip.close()
            video.close()
            txt_clip.close()
            final_video.close()
            
            logger.info(f"Carousel video saved to: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error creating carousel video: {e}")
            return False
    
    def get_video_duration(self, video_path: str) -> Optional[float]:
        """
        Get duration of a video file.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Duration in seconds or None if failed
        """
        try:
            video = VideoFileClip(video_path)
            duration = video.duration
            video.close()
            return duration
        except Exception as e:
            logger.error(f"Error getting video duration: {e}")
            return None
