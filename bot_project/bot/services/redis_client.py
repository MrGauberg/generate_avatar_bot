# bot/services/redis_client.py

import redis.asyncio as redis
from bot.config import Settings

class RedisClient:
    """Клиент Redis для работы с состояниями пользователей и загрузкой фото"""

    def __init__(self):
        self.redis = redis.Redis(
            host=Settings.redis.host,
            port=Settings.redis.port,
            db=0,  # Используем 0-ю базу, можно изменить
            decode_responses=True
        )

    async def set_user_state(self, user_id: int, state: str):
        """Устанавливает состояние пользователя в Redis"""
        key = f"user:{user_id}:state"
        await self.redis.set(key, state)

    async def get_user_state(self, user_id: int) -> str | None:
        """Получает текущее состояние пользователя"""
        key = f"user:{user_id}:state"
        return await self.redis.get(key)

    async def clear_user_state(self, user_id: int):
        """Удаляет состояние пользователя"""
        key = f"user:{user_id}:state"
        await self.redis.delete(key)

    ### --- Методы для работы с фото пользователей --- ###

    async def save_photo(self, user_id: int, photo_id: str):
        """Сохранение фото в Redis"""
        key = f"user:{user_id}:photos"
        await self.redis.rpush(key, photo_id)

    async def get_photos(self, user_id: int) -> list:
        """Получение списка загруженных фото"""
        key = f"user:{user_id}:photos"
        return await self.redis.lrange(key, 0, -1)

    async def clear_photos(self, user_id: int):
        """Очистка загруженных фото"""
        key = f"user:{user_id}:photos"
        await self.redis.delete(key)


    ### --- Методы для работы с авторизацией пользователей --- ###
    
    async def set_user_authorized(self, user_id: int, is_authorized: bool):
        """Сохраняет статус авторизации пользователя"""
        key = f"user:{user_id}:is_authorized"
        print(key)
        await self.redis.set(key, int(is_authorized))

    async def is_user_authorized(self, user_id: int) -> bool:
        """Проверяет, авторизован ли пользователь"""
        key = f"user:{user_id}:is_authorized"
        result = await self.redis.get(key)
        return bool(int(result)) if result is not None else False

    
redis_client = RedisClient()
