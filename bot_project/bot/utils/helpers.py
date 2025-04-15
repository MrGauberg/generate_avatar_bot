import json
from aiogram.types import Message

def pretty_json(data: dict) -> str:
    """Возвращает красиво отформатированный JSON (удобно для отладки)"""
    return json.dumps(data, indent=4, ensure_ascii=False)


async def get_user_info(message: Message) -> dict:
    """Получает информацию о пользователе из объекта сообщения"""
    user = message.from_user
    return {
        "id": user.id,
        "username": user.username or "Не указан",
        "full_name": user.full_name,
        "language_code": user.language_code or "Не указан"
    }


def format_price(price: int) -> str:
    """Форматирует цену в рублях"""
    return f"{price:,} ₽".replace(",", " ")


def extract_command_args(text: str) -> str:
    """Извлекает аргументы команды после пробела"""
    parts = text.split(maxsplit=1)
    return parts[1] if len(parts) > 1 else ""
