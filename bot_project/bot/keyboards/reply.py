# bot/keyboards/reply.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    """Главное меню бота"""
    buttons = [
        [KeyboardButton(text="🖼 Создать аватар"), KeyboardButton(text="🎨 Генерация изображений")],
        [KeyboardButton(text="🔮 Режим Бога"), KeyboardButton(text="⚙ Настройки")],
        [KeyboardButton(text="📞 Поддержка")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
