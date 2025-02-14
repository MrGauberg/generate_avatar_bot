# bot/keyboards/reply.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    """Главное меню бота (reply-кнопки)"""
    buttons = [
        [KeyboardButton(text="🎨 Стили"), KeyboardButton(text="🔮 Режим Бога")],
        [KeyboardButton(text="🖼 Аватар"), KeyboardButton(text="💰 Генерации")],
        [KeyboardButton(text="⚙ Настройки"), KeyboardButton(text="📞 Поддержка")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=False)
