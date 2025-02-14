# bot/handlers/start.py

from aiogram import Router, types
from aiogram.filters import Command
from bot.keyboards.inline import main_menu_keyboard, start_keyboard
from bot.handlers.avatar import avatar_callback_handler
from bot.handlers.generation import generate_menu_callback
from bot.handlers.god_mode import god_mode_menu_callback
from bot.handlers.settings import settings_menu_callback
from bot.handlers.support import support_callback_handler
from bot.handlers.profile import profile_menu_callback
from bot.handlers.ukassa import request_email

import logging
from bot.services.api_client import api_client

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    """Приветственное сообщение с проверкой авторизации"""
    user_id = message.from_user.id

    try:
        user_data = await api_client.get_user_profile(user_id)
        print(user_data)
        if user_data.get("is_authenticated"):
            await message.answer(
                "👋 Привет! Рад видеть тебя снова!\n\n"
                "Выбери, что хочешь сделать сегодня: создать аватар, попробовать режим 'Бога' или просто поэкспериментировать с генерацией изображений!",
                reply_markup=main_menu_keyboard()
            )
            return

    except Exception as e:
        logging.error(f"Ошибка при проверке авторизации: {e}")

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


@router.message(lambda message: message.text == "🎨 Стили")
async def styles_button_handler(message: types.Message):
    """Обработка кнопки 'Стили'"""
    await message.answer("Выберите стиль для генерации изображений.")
    await generate_menu_callback(message)  # Переход в выбор стилей


@router.message(lambda message: message.text == "🔮 Режим Бога")
async def god_mode_button_handler(message: types.Message):
    """Обработка кнопки 'Режим Бога'"""
    await god_mode_menu_callback(message)


@router.message(lambda message: message.text == "🖼 Аватар")
async def avatar_button_handler(message: types.Message):
    """Обработка кнопки 'Аватар'"""
    await avatar_callback_handler(message)


@router.message(lambda message: message.text == "💰 Генерации")
async def generations_button_handler(message: types.Message):
    """Обработка кнопки 'Генерации'"""
    await message.answer("💰 Здесь вы можете посмотреть оставшиеся генерации или купить новые.")
    await profile_menu_callback(message)  # Переход в профиль


@router.message(lambda message: message.text == "⚙ Настройки")
async def settings_button_handler(message: types.Message):
    """Обработка кнопки 'Настройки'"""
    await settings_menu_callback(message)


@router.message(lambda message: message.text == "📞 Поддержка")
async def support_button_handler(message: types.Message):
    """Обработка кнопки 'Поддержка'"""
    await support_callback_handler(message)




