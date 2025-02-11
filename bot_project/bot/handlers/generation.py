# bot/handlers/generation.py

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.services.api_client import api_client

router = Router()


async def get_styles_keyboard():
    """Создание клавиатуры со стилями"""
    styles = await api_client.get_styles_list()

    buttons = [
        [InlineKeyboardButton(text=style["name"], callback_data=f"generate_{style['id']}")]
        for style in styles
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("generate"))
async def generate_command_handler(message: types.Message):
    """Команда /generate для выбора стиля перед генерацией"""
    keyboard = await get_styles_keyboard()
    await message.answer("🎨 Выбери стиль для генерации изображения:", reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("generate_"))
async def generate_image(callback_query: types.CallbackQuery):
    """Обработка выбора стиля и генерация изображения"""
    style_id = callback_query.data.split("_")[1]

    await callback_query.message.edit_text("⏳ Генерируем изображение, подождите...")

    try:
        response = await api_client.generate_user_image(prompt="", model_id=int(style_id))
        image_url = response.get("image_url")

        if image_url:
            await callback_query.message.answer_photo(photo=image_url, caption="✨ Сгенерированное изображение!")
        else:
            await callback_query.message.answer("❌ Ошибка генерации изображения.")
    except Exception as e:
        await callback_query.message.answer(f"❌ Ошибка: {e}")
