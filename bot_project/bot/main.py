# bot/main.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.config import Settings
from bot.services.api_client import api_client
from bot.handlers import start
from bot.handlers import avatar
from bot.handlers import categories
from bot.handlers import god_mode
from bot.handlers import settings
from bot.handlers import payments
from bot.handlers import profile
from bot.handlers import support
from bot.handlers import generation
from bot.utils.logger import logger
from bot.middlewares.throttle import ThrottleMiddleware

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
bot = Bot(token=Settings.bot.TOKEN)
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(avatar.router)
dp.include_router(categories.router)
dp.include_router(god_mode.router)
dp.include_router(settings.router)
dp.include_router(payments.router)
dp.include_router(profile.router)
dp.include_router(support.router)
dp.include_router(generation.router) 
dp.message.middleware(ThrottleMiddleware(rate_limit=0.3))  # Подключаем антифлуд


logger.info("Запуск бота...")

async def on_startup():
    """Действия при запуске бота"""
    try:
        logging.info("Authenticating bot with API...")
        email = Settings.user.email
        password = Settings.user.password
        await api_client.authenticate(email, password)
        logging.info("Bot successfully authenticated!")
    except Exception as e:
        logging.error(f"Authentication failed: {e}")
        raise e

    logging.info("Bot started successfully!")


async def main():
    """Главная асинхронная функция запуска бота"""
    await on_startup()
    
    try:
        await dp.start_polling(bot)
    finally:
        await api_client.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
