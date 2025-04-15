from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Any, Dict, Callable
import asyncio


class ThrottleMiddleware(BaseMiddleware):
    """Миддлварь для предотвращения спама"""

    def __init__(self, rate_limit: float = 1.5):
        """
        :param rate_limit: минимальное время (в секундах) между сообщениями одного пользователя
        """
        super().__init__()
        self.rate_limit = rate_limit
        self.users = {}

    async def __call__(
        self, handler: Callable[[Message, Dict[str, Any]], Any], event: Message, data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id

        if user_id in self.users:
            last_time = self.users[user_id]
            if (event.date.timestamp() - last_time) < self.rate_limit:
                await event.answer("⏳ Подождите немного перед отправкой следующего сообщения.")
                return

        self.users[user_id] = event.date.timestamp()
        return await handler(event, data)
