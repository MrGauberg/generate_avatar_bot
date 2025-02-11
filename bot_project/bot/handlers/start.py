# bot/handlers/start.py

from aiogram import Router, types
from aiogram.filters import Command
from bot.keyboards.inline import main_menu_keyboard
from bot.handlers.avatar import avatar_callback_handler
from bot.handlers.generation import generate_menu_callback
from bot.handlers.god_mode import god_mode_menu_callback
from bot.handlers.settings import settings_menu_callback
from bot.handlers.support import support_callback_handler
from bot.handlers.profile import profile_menu_callback
from bot.handlers.payments import buy_menu_callback

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    """Обработчик команды /start"""
    welcome_text = (
        "👋 Привет! Я бот, который поможет тебе создать аватар и генерировать изображения.\n\n"
        "👇 Выбери, что хочешь сделать:"
    )

    await message.answer(welcome_text, reply_markup=main_menu_keyboard())


# 🔄 Обработчики inline-кнопок
@router.callback_query(lambda c: c.data == "menu_create_avatar")
async def avatar_button_handler(callback: types.CallbackQuery):
    """Обработка кнопки 'Создать аватар'"""
    await avatar_callback_handler(callback)
    await callback.answer()  # Добавляем callback.answer(), чтобы кнопка не зависала


@router.callback_query(lambda c: c.data == "menu_generate_images")
async def generate_button_handler(callback: types.CallbackQuery):
    """Обработка кнопки 'Генерация изображений'"""
    await generate_menu_callback(callback)
    await callback.answer()


@router.callback_query(lambda c: c.data == "menu_god_mode")
async def god_mode_button_handler(callback: types.CallbackQuery):
    """Обработка кнопки 'Режим Бога'"""
    await god_mode_menu_callback(callback)
    await callback.answer()


@router.callback_query(lambda c: c.data == "menu_settings")
async def settings_button_handler(callback: types.CallbackQuery):
    """Обработка кнопки 'Настройки'"""
    await settings_menu_callback(callback)
    await callback.answer()


@router.callback_query(lambda c: c.data == "menu_support")
async def support_button_handler(callback: types.CallbackQuery):
    """Обработка кнопки 'Поддержка'"""
    await support_callback_handler(callback)
    await callback.answer()


@router.callback_query(lambda c: c.data == "menu_profile")
async def profile_button_handler(callback: types.CallbackQuery):
    """Обработка кнопки 'Профиль'"""
    await profile_menu_callback(callback)
    await callback.answer()


@router.callback_query(lambda c: c.data == "menu_buy")
async def buy_button_handler(callback: types.CallbackQuery):
    """Обработка кнопки 'Купить генерации'"""
    await buy_menu_callback(callback)
    await callback.answer()
