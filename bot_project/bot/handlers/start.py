from aiogram import Router, types
from aiogram.filters import Command
from bot.keyboards.inline import start_keyboard

from bot.utils.logger import logger
from bot.services.api_client import api_client
from bot.keyboards.reply import main_menu_keyboard
from bot.services.redis_client import redis_client

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    """Приветственное сообщение с проверкой авторизации"""
    user_id = message.from_user.id
    

    try:
        user_data = await api_client.get_user_profile(user_id)
        if user_data.get("is_authorized"):
            await redis_client.set_user_authorized(user_id, True)
            await message.answer(
                "👋 Привет! Рад видеть тебя снова!\n\n"
                "Выбери, что хочешь сделать сегодня: создать аватар, попробовать режим 'Бога' или просто поэкспериментировать с генерацией изображений!",
                reply_markup=main_menu_keyboard()
            )
            return
    except Exception as e:
        logger.error(f"Ошибка при проверке авторизации: {e}")

    await redis_client.set_user_authorized(user_id, False)
    await message.answer(
        "👋 Привет! Добро пожаловать в нашего бота!\n\n"
        "🎨 Здесь ты сможешь создать уникальный аватар по своим фото и генерировать изображения в разных стилях!\n\n"
        "🔹 **Как это работает?**\n"
        "1️⃣ Загрузи 10 своих фото\n"
        "2️⃣ Выбери стиль или опиши картинку текстом (режим 'Бога')\n"
        "3️⃣ Получи уникальные изображения!\n\n"
        "💡 Готов начать? Выбери один из вариантов ниже:",
        reply_markup=start_keyboard()
    )

