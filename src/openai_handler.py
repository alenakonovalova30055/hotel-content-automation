import os
import time
from typing import Optional
from openai import OpenAI, OpenAIError, RateLimitError, APIError
from src.logger import logger

class OpenAIHandler:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4-turbo"
        self.max_retries = 3
        self.retry_delay = 2  # seconds
    
    def generate_description(self, content: str) -> Optional[str]:
        """
        Generate hotel description from content using OpenAI
        
        Args:
            content: Text content to generate description from
            
        Returns:
            Generated description or None if generation fails
        """
        if not content or not content.strip():
            logger.warning("⚠️ Пустой контент для генерации описания")
            return None
        
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "Ты профессиональный копирайтер отеля. Создавай привлекательные описания на русском языке."
                        },
                        {
                            "role": "user",
                            "content": f"Напиши привлекательное описание для отеля на основе: {content}"
                        }
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                description = response.choices[0].message.content
                logger.info("✅ Описание сгенерировано")
                return description
            except RateLimitError as e:
                if attempt < self.max_retries - 1:
                    logger.warning(f"⚠️ Rate limit достигнут (попытка {attempt + 1}/{self.max_retries}): {e}")
                    time.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff
                else:
                    logger.error(f"❌ Не удалось сгенерировать описание после {self.max_retries} попыток: {e}")
                    return None
            except APIError as e:
                if attempt < self.max_retries - 1:
                    logger.warning(f"⚠️ Ошибка API OpenAI (попытка {attempt + 1}/{self.max_retries}): {e}")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"❌ Ошибка API OpenAI: {e}")
                    return None
            except OpenAIError as e:
                logger.error(f"❌ Ошибка OpenAI: {e}")
                return None
            except Exception as e:
                logger.error(f"❌ Неожиданная ошибка при генерации описания: {e}")
                return None
        
        return None
    
    def generate_title(self, description: str) -> Optional[str]:
        """
        Generate a short title from description using OpenAI
        
        Args:
            description: Description text to generate title from
            
        Returns:
            Generated title or None if generation fails
        """
        if not description or not description.strip():
            logger.warning("⚠️ Пустое описание для генерации заголовка")
            return None
        
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "Ты профессиональный копирайтер. Создавай короткие привлекательные заголовки."
                        },
                        {
                            "role": "user",
                            "content": f"Создай короткий заголовок (до 10 слов) для: {description}"
                        }
                    ],
                    temperature=0.7,
                    max_tokens=100
                )
                title = response.choices[0].message.content
                logger.info("✅ Заголовок сгенерирован")
                return title
            except RateLimitError as e:
                if attempt < self.max_retries - 1:
                    logger.warning(f"⚠️ Rate limit достигнут (попытка {attempt + 1}/{self.max_retries}): {e}")
                    time.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff
                else:
                    logger.error(f"❌ Не удалось сгенерировать заголовок после {self.max_retries} попыток: {e}")
                    return None
            except APIError as e:
                if attempt < self.max_retries - 1:
                    logger.warning(f"⚠️ Ошибка API OpenAI (попытка {attempt + 1}/{self.max_retries}): {e}")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"❌ Ошибка API OpenAI: {e}")
                    return None
            except OpenAIError as e:
                logger.error(f"❌ Ошибка OpenAI: {e}")
                return None
            except Exception as e:
                logger.error(f"❌ Неожиданная ошибка при генерации заголовка: {e}")
                return None
        
        return None
