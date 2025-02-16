# bot/main.py

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from bot.config import Settings
from bot.services.api_client import api_client
from bot.handlers import start
from bot.handlers import avatar
from bot.handlers import categories
from bot.handlers import god_mode
from bot.handlers import settings
from bot.handlers import support
from bot.handlers import generation
from bot.utils.logger import logger
from bot.middlewares.throttle import ThrottleMiddleware
from bot.handlers import instruction
from bot.handlers import ukassa
from bot.handlers.webhooks import handle_payment_webhook
from aiogram.fsm.storage.redis import RedisStorage
from aiohttp import web

from bot.services.redis_client import redis_client


# Настраиваем логирование
logging.basicConfig(level=logging.INFO)


# Инициализируем бота
bot = Bot(token=Settings.bot.TOKEN)


dp: Dispatcher | None = None


async def create_dispatcher():
    """Создает и возвращает диспетчер с Redis-хранилищем"""
    global dp
    if dp is None:
        storage = RedisStorage(redis_client.redis)
        dp = Dispatcher(storage=storage)
    return dp


async def start_webhook_server(dp: Dispatcher):
    """Запускаем веб-сервер для обработки вебхуков"""
    link = "/payment-webhook/"
    port = 8090 
    ip = "0.0.0.0"

    app = web.Application()
    app["dp"] = dp  # Передаем Dispatcher в app
    app.router.add_post(link, handle_payment_webhook)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, ip, port)
    await site.start()
    logging.info(f"Webhook server запущен на http://{ip}:{port}{link}")


async def set_menu():
    await bot.send_message('592375841', text="Бот запущен!")
    await bot.set_my_commands([
        types.BotCommand(command="/start", description="Знакомство с ботом"),
    ])


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
    dp = await create_dispatcher()
    dp.include_router(start.router)
    dp.include_router(avatar.router)
    dp.include_router(categories.router)
    dp.include_router(settings.router)
    dp.include_router(support.router)
    dp.include_router(generation.router) 
    dp.include_router(instruction.router)
    dp.include_router(ukassa.router)
    dp.include_router(god_mode.router)
    # dp.message.middleware(ThrottleMiddleware(rate_limit=0.3))  # антифлуд

    await on_startup()
    await set_menu()
    
    try:
        await asyncio.gather(
            dp.start_polling(bot),
            start_webhook_server(dp)
        )
    finally:
        await api_client.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
