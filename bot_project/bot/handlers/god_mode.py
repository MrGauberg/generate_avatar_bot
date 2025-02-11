# bot/handlers/god_mode.py

from aiogram import Router, types
from bot.services.api_client import api_client
from bot.keyboards.inline import god_mode_keyboard

router = Router()
enabled_users = set()  # Храним пользователей с активированным режимом "Бога"


@router.callback_query(lambda c: c.data == "menu_god_mode")
async def god_mode_menu_callback(callback: types.CallbackQuery):
    """Обработка нажатия кнопки 'Режим Бога'"""
    await callback.message.edit_text(
        "🔮 Хочешь активировать режим 'Бога'? Он позволяет создавать изображения по тексту!",
        reply_markup=god_mode_keyboard()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "godmode_enable")
async def enable_god_mode_callback(callback: types.CallbackQuery):
    """Обработка включения режима 'Бога'"""
    try:
        await api_client.enable_god_mode()
        enabled_users.add(callback.from_user.id)  # Добавляем пользователя в список активных
        await callback.message.edit_text("✅ Режим 'Бога' активирован! Теперь отправьте описание для генерации.")
    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка при включении режима 'Бога': {e}")

    await callback.answer()


@router.callback_query(lambda c: c.data == "godmode_disable")
async def disable_god_mode_callback(callback: types.CallbackQuery):
    """Обработка выключения режима 'Бога'"""
    try:
        await api_client.disable_god_mode()
        enabled_users.discard(callback.from_user.id)  # Удаляем пользователя из списка активных
        await callback.message.edit_text("❌ Режим 'Бога' выключен.")
    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка при выключении режима 'Бога': {e}")

    await callback.answer()


@router.message(lambda message: message.text and message.from_user.id in enabled_users)
async def generate_image_in_god_mode(message: types.Message):
    """Генерация изображения по текстовому описанию в режиме 'Бога'"""
    try:
        response = await api_client.generate_user_image(prompt=message.text, model_id=1)
        image_url = response.get("image_url")

        if image_url:
            await message.answer_photo(photo=image_url, caption="✨ Сгенерированное изображение!")
        else:
            await message.answer("❌ Ошибка генерации изображения.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
