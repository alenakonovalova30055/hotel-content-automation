"""Text design and styling for video overlays."""

import json
import random
from typing import Tuple, Optional
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .logger import get_logger

logger = get_logger()


class TextDesigner:
    """Handle text styling and positioning for video overlays."""
    
    def __init__(self, style_guide_path: str = None):
        """
        Initialize text designer.
        
        Args:
            style_guide_path: Path to style guide JSON file
        """
        if style_guide_path is None:
            style_guide_path = Path(__file__).parent.parent / "templates" / "style_guide.json"
        
        self.style_guide = self._load_style_guide(style_guide_path)
        logger.info("Text designer initialized")
    
    def _load_style_guide(self, path: str) -> dict:
        """Load style guide from JSON file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                guide = json.load(f)
            logger.info(f"Loaded style guide from: {path}")
            return guide
        except Exception as e:
            logger.warning(f"Error loading style guide: {e}. Using defaults.")
            return {
                "text_colors": ["white", "#FFE5B4", "#FFB6C1", "#ADD8E6"],
                "text_positions": ["bottom", "center", "top-left", "top-right"],
                "font_sizes": {"small": 40, "medium": 60, "large": 80}
            }
    
    def get_random_color(self) -> str:
        """Get a random text color from style guide."""
        colors = self.style_guide.get("text_colors", ["white"])
        return random.choice(colors)
    
    def get_random_position(self) -> str:
        """Get a random text position from style guide."""
        positions = self.style_guide.get("text_positions", ["bottom"])
        return random.choice(positions)
    
    def get_font_size(self, size_name: str = "medium") -> int:
        """Get font size from style guide."""
        sizes = self.style_guide.get("font_sizes", {"medium": 60})
        return sizes.get(size_name, 60)
    
    def calculate_position(
        self,
        video_width: int,
        video_height: int,
        text_width: int,
        text_height: int,
        position: str
    ) -> Tuple[int, int]:
        """
        Calculate text position coordinates based on position name.
        
        Args:
            video_width: Width of video frame
            video_height: Height of video frame
            text_width: Width of text
            text_height: Height of text
            position: Position name (bottom, center, top-left, etc.)
            
        Returns:
            Tuple of (x, y) coordinates
        """
        margin = 50  # Margin from edges
        
        positions_map = {
            "bottom": (video_width // 2 - text_width // 2, video_height - text_height - margin),
            "center": (video_width // 2 - text_width // 2, video_height // 2 - text_height // 2),
            "top": (video_width // 2 - text_width // 2, margin),
            "top-left": (margin, margin),
            "top-right": (video_width - text_width - margin, margin),
            "bottom-left": (margin, video_height - text_height - margin),
            "bottom-right": (video_width - text_width - margin, video_height - text_height - margin),
        }
        
        return positions_map.get(position, positions_map["bottom"])
    
    def create_text_clip_config(
        self,
        text: str,
        video_width: int,
        video_height: int,
        duration: float
    ) -> dict:
        """
        Create configuration for text clip overlay.
        
        Args:
            text: Text to display
            video_width: Width of video
            video_height: Height of video
            duration: Duration of text display
            
        Returns:
            Configuration dictionary for text clip
        """
        color = self.get_random_color()
        position = self.get_random_position()
        font_size = self.get_font_size("medium")
        
        config = {
            "text": text,
            "font_size": font_size,
            "color": color,
            "position": position,
            "duration": duration,
            "video_width": video_width,
            "video_height": video_height,
            "stroke_color": "black",
            "stroke_width": 2,
            "method": "caption"  # For moviepy TextClip
        }
        
        logger.info(f"Created text config: position={position}, color={color}, size={font_size}")
        return config
    
    def wrap_text(self, text: str, max_width: int, font_size: int) -> str:
        """
        Wrap text to fit within max width.
        
        Args:
            text: Text to wrap
            max_width: Maximum width in pixels
            font_size: Font size
            
        Returns:
            Wrapped text with newlines
        """
        words = text.split()
        lines = []
        current_line = []
        
        # Rough estimation: ~0.6 * font_size per character width
        char_width = font_size * 0.6
        max_chars = int(max_width / char_width)
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if len(test_line) <= max_chars:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
