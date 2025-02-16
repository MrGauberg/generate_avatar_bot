# bot/services/redis_client.py

import redis.asyncio as redis
from bot.config import Settings

# Создаем асинхронное подключение к Redis
redis_client = redis.Redis(
    host=Settings.redis.host,
    port=Settings.redis.port,
    db=0,  # Указываем базу данных (можно изменить при необходимости)
    decode_responses=True
)
