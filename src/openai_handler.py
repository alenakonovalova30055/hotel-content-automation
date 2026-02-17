import os
from openai import OpenAI
from src.logger import logger

class OpenAIHandler:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4-turbo"
    
    def generate_description(self, text):
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
                        "content": f"Напиши привлекательное описание для отеля на основе: {text}"
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            description = response.choices[0].message.content
            logger.info("✅ Описание сгенерировано")
            return description
        except Exception as e:
            logger.error(f"❌ Ошибка OpenAI: {e}")
            return None
    
    def generate_title(self, description):
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
        except Exception as e:
            logger.error(f"❌ Ошибка OpenAI: {e}")
            return None
