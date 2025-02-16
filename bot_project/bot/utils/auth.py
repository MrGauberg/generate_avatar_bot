# bot/utils/auth.py

from aiogram import types
from functools import wraps
from bot.handlers.start import start_handler
from bot.services.redis_client import redis_client

def require_authorization(handler):
    """Декоратор для проверки авторизации пользователя перед вызовом обработчика"""
    @wraps(handler)
    async def wrapper(message: types.Message, *args, **kwargs):
        user_id = message.from_user.id
        is_authorized = await redis_client.is_user_authorized(user_id)
        print(f"User {user_id} is authorized: {is_authorized}")
        if not is_authorized:
            await start_handler(message)  # Вызываем `start_handler` для авторизации
            return
        return await handler(message, *args, **kwargs)
    
    return wrapper
