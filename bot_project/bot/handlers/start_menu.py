# bot/handlers/start.py

from aiogram import Router, types
from bot.handlers.generation import generate_menu_callback
from bot.handlers.god_mode import god_mode_menu_callback
from bot.handlers.settings import settings_menu_callback
from bot.handlers.support import support_callback_handler
from bot.utils.auth import require_authorization


router = Router()

@router.message(lambda message: message.text == "🎨 Стили")
@require_authorization
async def styles_button_handler(message: types.Message):
    """Обработка кнопки 'Стили'"""
    await message.answer("Выберите стиль для генерации изображений.")
    await generate_menu_callback(message)  # Переход в выбор стилей


@router.message(lambda message: message.text == "🔮 Режим Бога")
@require_authorization
async def god_mode_button_handler(message: types.Message):
    """Обработка кнопки 'Режим Бога'"""
    await god_mode_menu_callback(message)



@router.message(lambda message: message.text == "⚙ Настройки")
@require_authorization
async def settings_button_handler(message: types.Message):
    """Обработка кнопки 'Настройки'"""
    await settings_menu_callback(message)



@router.message(lambda message: message.text == "📞 Поддержка")
@require_authorization
async def support_button_handler(message: types.Message):
    """Обработка кнопки 'Поддержка'"""
    await support_callback_handler(message)




