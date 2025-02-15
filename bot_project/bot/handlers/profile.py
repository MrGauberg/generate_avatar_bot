# bot/handlers/profile.py

from aiogram import Router, types
from bot.services.api_client import api_client
from bot.keyboards.inline import profile_keyboard

router = Router()



@router.callback_query(lambda c: c.data == "menu_profile")
@router.message(lambda message: message.text == "👤 Профиль")
async def profile_menu_callback(event: types.Message | types.CallbackQuery):
    """Обработчик кнопки 'Профиль'"""
    user_id = event.from_user.id

    if isinstance(event, types.CallbackQuery):
        message = event.message
    else:
        message = event

    await send_profile_info(message, user_id)



@router.callback_query(lambda c: c.data == "profile_refresh")
async def refresh_profile_callback(callback: types.CallbackQuery):
    """Обновление информации профиля"""
    await callback.message.edit_text("🔄 Обновляем данные профиля...")
    await send_profile_info(callback.message, callback.from_user.id)
    await callback.answer()


async def send_profile_info(message: types.Message, user_id: int):
    """Функция отправки информации о профиле"""
    try:
        response = await api_client.get_user_profile(user_id)
        
        if response:
            username = response.get("username", "Не указано")
            email = response.get("email", "Не указано")
            total_generations = response.get("total_generations", 0)
            remaining_generations = response.get("remaining_generations", 0)

            profile_text = (
                f"👤 **Ваш профиль**\n"
                f"🆔 Telegram ID: `{user_id}`\n"
                f"📛 Имя: {username}\n"
                f"📧 Email: {email}\n"
                f"🎨 Всего генераций: {total_generations}\n"
                f"🖼 Осталось генераций: {remaining_generations}"
            )

            await message.edit_text(profile_text, parse_mode="Markdown", reply_markup=profile_keyboard())
        else:
            await message.edit_text("❌ Ошибка при получении профиля.")
    
    except Exception as e:
        await message.edit_text(f"❌ Ошибка: {e}")
