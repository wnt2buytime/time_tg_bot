import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения. Создайте файл .env с BOT_TOKEN=your_token")

# Проверяем что токен не пустой
if not isinstance(BOT_TOKEN, str) or len(BOT_TOKEN.strip()) == 0:
    raise ValueError("BOT_TOKEN должен быть непустой строкой") 