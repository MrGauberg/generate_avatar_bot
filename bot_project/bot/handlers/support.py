# bot/handlers/support.py

from aiogram import Router, types
from aiogram.filters import Command

router = Router()

SUPPORT_USERNAME = "your_support_username"  # Укажите username службы поддержки

@router.message(Command("support"))
async def support_command_handler(message: types.Message):
    """Команда /support для обращения в поддержку"""
    support_text = (
        "📞 **Поддержка**\n\n"
        "Если у вас возникли вопросы или проблемы, свяжитесь с нашей поддержкой по ссылке ниже:\n\n"
        f"🔗 [Написать в поддержку](https://t.me/{SUPPORT_USERNAME})"
    )

    await message.answer(support_text, parse_mode="Markdown", disable_web_page_preview=True)
