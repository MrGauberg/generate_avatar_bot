# bot/config.py

import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

class BotConfig:
    TOKEN: str = os.getenv("BOT_TOKEN")  # Токен бота
    API_URL: str = os.getenv("API_URL")  # URL бэкенда
    ADMIN_ID: int = os.getenv("ADMIN_ID")  # ID администратора
    USE_REDIS: bool = os.getenv("USE_REDIS", "False").lower() == "true"  # Использовать Redis?

class UserConfig:
    email: str = os.getenv("USER_EMAIL")
    password: str = os.getenv("USER_PASSWORD")
    tg_user_name: str = os.getenv("ADMIN_TG")

class YookassaConfig:
    SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
    SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")

class ServiceConfig:
    IMAGES_COUNT: int = int(os.getenv("IMAGES_COUNT", 10))


class Settings:
    bot = BotConfig()
    yookassa = YookassaConfig()
    user = UserConfig()
    service = ServiceConfig()
