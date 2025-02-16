# bot/handlers/settings.py

from aiogram import Router, types
from bot.services.api_client import api_client
from bot.keyboards.inline import photo_format_keyboard, settings_menu_keyboard
from bot.utils.auth import require_authorization

router = Router()


@router.message(lambda message: message.text == "⚙ Настройки")
@require_authorization
async def settings_menu_callback(message: types.Message):
    """Обработчик кнопки 'Настройки'"""

    await message.answer("⚙ Выберите настройки:", reply_markup=settings_menu_keyboard())



@router.callback_query(lambda c: c.data == "settings_photo_format")
async def choose_photo_format(callback: types.CallbackQuery):
    """Вывод списка форматов фото"""
    await callback.message.edit_text("📏 Выберите формат фото:", reply_markup=photo_format_keyboard())
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("set_photo_format_"))
async def handle_photo_format_selection(callback: types.CallbackQuery):
    """Обработка выбора формата фото"""
    selected_format = callback.data.split("_")[-1]  # Теперь формат передается правильно
    user_id = callback.from_user.id

    try:
        await api_client.set_photo_format(user_id, selected_format)
        await callback.message.edit_text(f"✅ Принято! Следующие фото будут в формате {selected_format}.")
    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка при установке формата: {e}")

    await callback.answer()

