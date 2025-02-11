# bot/handlers/settings.py

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.services.api_client import api_client

router = Router()

PHOTO_FORMATS = {
    "1:1": "1x1",
    "3:4": "3x4",
    "9:16": "9x16",
    "16:9": "16x9"
}

async def get_settings_keyboard():
    """Создает клавиатуру для выбора формата фото"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=format_option)] for format_option in PHOTO_FORMATS.keys()],
        resize_keyboard=True
    )
    return keyboard


@router.message(Command("settings"))
async def settings_command_handler(message: types.Message):
    """Команда /settings для изменения настроек"""
    keyboard = await get_settings_keyboard()
    await message.answer("⚙ Выберите формат фото:", reply_markup=keyboard)


@router.message(lambda message: message.text in PHOTO_FORMATS)
async def handle_photo_format_selection(message: types.Message):
    """Обработка выбора формата фото"""
    selected_format = PHOTO_FORMATS[message.text]

    try:
        await api_client._make_request("POST", f"{api_client.BASE_API_URL}/settings/photo-format", {"format": selected_format})
        await message.answer(f"✅ Формат фото установлен: {message.text}")
    except Exception as e:
        await message.answer(f"❌ Ошибка при установке формата: {e}")
