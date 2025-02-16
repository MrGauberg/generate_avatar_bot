# bot/handlers/god_mode.py

from aiogram import Router, types

from aiogram.filters import StateFilter

from bot.services.api_client import api_client
from bot.keyboards.inline import god_mode_keyboard, god_mode_instruction_keyboard

router = Router()



@router.callback_query(lambda c: c.data == "menu_god_mode")
@router.message(lambda message: message.text == "🔮 Режим Бога")
async def god_mode_menu(event: types.Message | types.CallbackQuery):
    """Обработчик кнопки 'Режим Бога'"""
    user_id = event.from_user.id
    user_data = await api_client.get_user_profile(user_id)
    is_god_mode_enabled = user_data.get("god_mode", False)

    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text(
            "🔮 **Режим Бога**\n\n"
            "Этот режим позволяет генерировать изображения по текстовому описанию.",
            reply_markup=god_mode_keyboard(is_god_mode_enabled)
        )
    else:
        await event.answer(
            "🔮 **Режим Бога**\n\n"
            "Этот режим позволяет генерировать изображения по текстовому описанию.",
            reply_markup=god_mode_keyboard(is_god_mode_enabled)
        )



@router.callback_query(lambda c: c.data == "godmode_menu")
async def god_mode_menu_callback(callback: types.CallbackQuery):
    """Возвращение в главное меню режима Бога"""
    user_id = callback.from_user.id
    user_data = await api_client.get_user_profile(user_id)
    is_god_mode_enabled = user_data.get("god_mode", False)

    await callback.message.edit_text(
        "🔮 **Режим Бога**\n\n"
        "Этот режим позволяет генерировать изображения по текстовому описанию.",
        reply_markup=god_mode_keyboard(is_god_mode_enabled)
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "godmode_instruction")
async def god_mode_instruction_callback(callback: types.CallbackQuery):
    """Вывод инструкции по режиму Бога"""
    await callback.message.edit_text(
        "ℹ **Инструкция по режиму Бога**\n\n"
        "В этом режиме ты можешь просто написать боту описание изображения, и он его сгенерирует!\n\n"
        "📌 Например: *'Космический кот в очках'*\n\n"
        "Нажми кнопку 'Назад', чтобы вернуться.",
        reply_markup=god_mode_instruction_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "godmode_toggle")
async def toggle_god_mode_callback(callback: types.CallbackQuery):
    """Включение/выключение режима Бога"""
    user_id = callback.from_user.id
    user_data = await api_client.get_user_profile(user_id)
    is_god_mode_enabled = user_data.get("god_mode", False)

    try:
        await api_client.set_god_mode(user_id, not is_god_mode_enabled)

        user_data = await api_client.get_user_profile(user_id)
        is_god_mode_enabled = user_data.get("god_mode", False)

        new_text = (
            "✅ **Режим Бога активирован!**\n\nНапиши описание боту, и он сгенерирует изображение."
            if is_god_mode_enabled else "❌ **Режим Бога деактивирован.**"
        )

        await callback.message.edit_text(new_text, reply_markup=god_mode_keyboard(is_god_mode_enabled))

    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка: {e}")

    await callback.answer()


@router.message(StateFilter(None), lambda message: message.text)
async def generate_image_in_god_mode(message: types.Message):
    """Генерация изображения по текстовому описанию в режиме 'Бога' (если бот не ждет других данных)"""
    
    user_id = message.from_user.id
    user_data = await api_client.get_user_profile(user_id)
    is_god_mode_enabled = user_data.get("god_mode", False)

    if not is_god_mode_enabled:
        return

    try:
        response = await api_client.generate_user_image(prompt=message.text, model_id=1)
        image_url = response.get("image_url")

        if image_url:
            await message.answer_photo(photo=image_url, caption="✨ Сгенерированное изображение!")
        else:
            await message.answer("❌ Ошибка генерации изображения.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

