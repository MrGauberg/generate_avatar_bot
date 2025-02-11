# bot/handlers/settings.py

from aiogram import Router, types
from bot.services.api_client import api_client
from bot.keyboards.inline import settings_keyboard, PHOTO_FORMATS

router = Router()


@router.callback_query(lambda c: c.data == "menu_settings")
async def settings_menu_callback(callback: types.CallbackQuery):
    """Обработка нажатия кнопки 'Настройки'"""
    await callback.message.edit_text("⚙ Выберите формат фото:", reply_markup=settings_keyboard())
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("settings_"))
async def handle_photo_format_selection_callback(callback: types.CallbackQuery):
    """Обработка выбора формата фото"""
    selected_format = callback.data.split("_")[1]

    try:
        await api_client._make_request("POST", f"{api_client.BASE_API_URL}/settings/photo-format", {"format": selected_format})
        await callback.message.edit_text(f"✅ Формат фото установлен: {selected_format}")
    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка при установке формата: {e}")

    await callback.answer()
