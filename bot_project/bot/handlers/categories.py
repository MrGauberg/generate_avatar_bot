# bot/handlers/categories.py

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.services.api_client import api_client

router = Router()


async def get_categories_keyboard():
    """Создание клавиатуры с категориями"""
    categories = await api_client.get_categories_list()
    buttons = [
        [InlineKeyboardButton(text=category["name"], callback_data=f"category_{category['id']}")]
        for category in categories
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_styles_keyboard(category_id=None):
    """Создание клавиатуры со стилями"""
    styles = await api_client.get_styles_list()
    
    if category_id:
        styles = [style for style in styles if style["category"] == category_id]

    buttons = [
        [InlineKeyboardButton(text=style["name"], callback_data=f"style_{style['id']}")]
        for style in styles
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("categories"))
async def categories_command_handler(message: types.Message):
    """Команда /categories для выбора категорий"""
    keyboard = await get_categories_keyboard()
    await message.answer("🎨 Выбери категорию:", reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("category_"))
async def category_selected(callback_query: types.CallbackQuery):
    """Обработка выбора категории"""
    category_id = callback_query.data.split("_")[1]
    keyboard = await get_styles_keyboard(category_id)
    await callback_query.message.edit_text("🎨 Выбери стиль:", reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("style_"))
async def style_selected(callback_query: types.CallbackQuery):
    """Обработка выбора стиля"""
    style_id = callback_query.data.split("_")[1]
    await callback_query.message.edit_text(f"✅ Выбран стиль ID: {style_id}. Теперь можешь генерировать изображение!")
