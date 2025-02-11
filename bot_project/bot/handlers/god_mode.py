# bot/handlers/god_mode.py

from aiogram import Router, types
from aiogram.filters import Command
from bot.services.api_client import api_client

router = Router()

@router.message(Command("godmode"))
async def god_mode_command_handler(message: types.Message):
    """Команда /godmode для включения или выключения режима 'Бога'"""
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🔮 Включить режим Бога")],
            [types.KeyboardButton(text="❌ Выключить режим Бога")]
        ],
        resize_keyboard=True
    )
    await message.answer("🔮 Хочешь активировать режим 'Бога'? Он позволяет создавать изображения по тексту!", reply_markup=keyboard)


@router.message(lambda message: message.text == "🔮 Включить режим Бога")
async def enable_god_mode(message: types.Message):
    """Обработка включения режима 'Бога'"""
    try:
        await api_client.enable_god_mode()
        await message.answer("✅ Режим 'Бога' активирован! Теперь ты можешь отправлять текстовые описания для генерации изображений.")
    except Exception as e:
        await message.answer(f"❌ Ошибка при включении режима 'Бога': {e}")


@router.message(lambda message: message.text == "❌ Выключить режим Бога")
async def disable_god_mode(message: types.Message):
    """Обработка выключения режима 'Бога'"""
    try:
        await api_client.disable_god_mode()
        await message.answer("❌ Режим 'Бога' выключен.")
    except Exception as e:
        await message.answer(f"❌ Ошибка при выключении режима 'Бога': {e}")


@router.message(lambda message: message.text and message.text.strip() != "")
async def generate_image_in_god_mode(message: types.Message):
    """Генерация изображения по текстовому описанию в режиме 'Бога'"""
    try:
        response = await api_client.generate_user_image(prompt=message.text, model_id=1)  # ID модели может быть параметризован
        image_url = response.get("image_url")

        if image_url:
            await message.answer_photo(photo=image_url, caption="✨ Сгенерированное изображение!")
        else:
            await message.answer("❌ Ошибка генерации изображения.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
