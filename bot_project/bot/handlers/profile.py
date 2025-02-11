# bot/handlers/profile.py

from aiogram import Router, types
from aiogram.filters import Command
from bot.services.api_client import api_client

router = Router()


@router.message(Command("profile"))
async def profile_command_handler(message: types.Message):
    """Команда /profile для просмотра профиля пользователя"""
    user_id = message.from_user.id

    await message.answer("⏳ Загружаем информацию о вашем профиле...")

    try:
        response = await api_client._make_request("GET", f"{api_client.BASE_API_URL}/user/profile")
        
        if response:
            username = response.get("username", "Не указано")
            email = response.get("email", "Не указано")
            total_generations = response.get("total_generations", 0)
            remaining_generations = response.get("remaining_generations", 0)

            profile_text = (
                f"👤 **Ваш профиль**\n"
                f"🆔 Telegram ID: `{user_id}`\n"
                f"📛 Имя: {username}\n"
                f"📧 Email: {email}\n"
                f"🎨 Всего генераций: {total_generations}\n"
                f"🖼 Осталось генераций: {remaining_generations}"
            )

            await message.answer(profile_text, parse_mode="Markdown")
        else:
            await message.answer("❌ Ошибка при получении профиля.")
    
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
