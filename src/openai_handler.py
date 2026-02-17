"""OpenAI integration for generating Instagram captions."""

import os
from typing import List, Optional
from openai import OpenAI

from .logger import get_logger

logger = get_logger()


class OpenAIHandler:
    """Handle OpenAI API operations for text generation."""
    
    def __init__(self, api_key: str):
        """
        Initialize OpenAI handler.
        
        Args:
            api_key: OpenAI API key
        """
        self.client = OpenAI(api_key=api_key)
        logger.info("OpenAI handler initialized")
    
    def generate_caption(
        self,
        hotel_description: str,
        reference_posts: List[str],
        content_type: str = "video"
    ) -> Optional[str]:
        """
        Generate Instagram caption based on hotel description and reference posts.
        
        Args:
            hotel_description: Description of the hotel
            reference_posts: List of example posts for style reference
            content_type: Type of content (video or carousel)
            
        Returns:
            Generated caption text or None if failed
        """
        try:
            # Prepare reference examples
            examples_text = "\n\n---\n\n".join(reference_posts[:5])  # Use first 5 examples
            
            # Create prompt
            prompt = f"""Ты - креативный копирайтер, создающий посты для Instagram отеля "Atlas Apart".

ОПИСАНИЕ ОТЕЛЯ:
{hotel_description}

ПРИМЕРЫ СТИЛЯ (для референса):
{examples_text}

ЗАДАЧА:
Создай короткую цепляющую подпись для Instagram {content_type} в том же стиле, что и примеры.

ТРЕБОВАНИЯ:
- Длина: 15-30 слов
- Стиль: легкий, приятный, привлекающий внимание
- Тон: дружелюбный, вдохновляющий
- Используй эмодзи умеренно
- Фокус на комфорте, расположении или удобствах отеля
- НЕ копируй примеры напрямую, создай новый уникальный текст

Ответь только текстом подписи, без дополнительных пояснений."""

            logger.info(f"Generating caption for {content_type}")
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Ты - профессиональный копирайтер для отелей."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.8,
                n=1
            )
            
            caption = response.choices[0].message.content.strip()
            logger.info(f"Generated caption: {caption[:50]}...")
            return caption
        
        except Exception as e:
            logger.error(f"Error generating caption: {e}")
            return None
    
    def generate_short_text_overlay(
        self,
        hotel_description: str,
        reference_posts: List[str]
    ) -> Optional[str]:
        """
        Generate short text overlay for video (3-7 words).
        
        Args:
            hotel_description: Description of the hotel
            reference_posts: List of example posts for style reference
            
        Returns:
            Generated short text or None if failed
        """
        try:
            examples_text = "\n".join([p[:100] for p in reference_posts[:3]])  # First 100 chars of 3 examples
            
            prompt = f"""Ты - креативный копирайтер для отеля "Atlas Apart".

ОПИСАНИЕ ОТЕЛЯ:
{hotel_description}

ПРИМЕРЫ СТИЛЯ:
{examples_text}

ЗАДАЧА:
Создай ОЧЕНЬ КОРОТКИЙ текст (3-7 слов) для наложения на видео.

ТРЕБОВАНИЯ:
- Длина: строго 3-7 слов
- Стиль: емкий, цепляющий
- Без эмодзи
- Фокус на одной ключевой идее: комфорт, отдых, удобства, расположение
- Примеры формата: "Твой идеальный отдых", "Комфорт в центре города", "Здесь начинается отпуск"

Ответь только текстом, без дополнительных пояснений."""

            logger.info("Generating short text overlay")
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Ты - профессиональный копирайтер."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.9,
                n=1
            )
            
            text = response.choices[0].message.content.strip()
            # Remove quotes if present
            text = text.strip('"').strip("'")
            logger.info(f"Generated text overlay: {text}")
            return text
        
        except Exception as e:
            logger.error(f"Error generating text overlay: {e}")
            return None
