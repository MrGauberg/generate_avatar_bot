# bot/handlers/start.py

from aiogram import Router, types
from aiogram.filters import Command
from bot.keyboards.reply import main_menu_keyboard

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    """Обработчик команды /start"""
    welcome_text = (
        "👋 Привет! Я бот, который поможет тебе создать аватар и генерировать изображения.\n\n"
        "📸 Отправь мне 10 фото, и мы создадим твой аватар.\n"
        "🎨 Затем ты сможешь выбирать стили и категории для генерации изображений.\n\n"
        "🔮 Есть также режим 'Бога', где ты можешь описывать картинки текстом!\n\n"
        "👇 Выбери, что хочешь сделать:"
    )

    await message.answer(welcome_text, reply_markup=main_menu_keyboard())
