# bot/keyboards/inline.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def gender_selection_keyboard():
    """Клавиатура выбора пола"""
    buttons = [
        [InlineKeyboardButton(text="👨 Мужчина", callback_data="avatar_gender_male")],
        [InlineKeyboardButton(text="👩 Женщина", callback_data="avatar_gender_female")],
        [InlineKeyboardButton(text="👶 Ребенок", callback_data="avatar_gender_child")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_categories_keyboard(categories):
    """Создает inline-клавиатуру для выбора категорий"""
    buttons = [
        [InlineKeyboardButton(text=category["name"], callback_data=f"category_{category['id']}")]
        for category in categories
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_styles_keyboard(styles, category_id=None):
    """Создает inline-клавиатуру для выбора стилей"""
    filtered_styles = [style for style in styles if category_id is None or style["category"] == category_id]
    
    buttons = [
        [InlineKeyboardButton(text=style["name"], callback_data=f"generate_{style['id']}")]
        for style in filtered_styles
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def god_mode_keyboard():
    """Клавиатура включения/выключения режима 'Бога'"""
    buttons = [
        [InlineKeyboardButton(text="🔮 Включить режим Бога", callback_data="godmode_enable")],
        [InlineKeyboardButton(text="❌ Выключить режим Бога", callback_data="godmode_disable")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_payment_keyboard():
    """Создает inline-клавиатуру с вариантами пакетов генераций"""
    packages = [
        {"id": 1, "name": "Пробный", "price": 199, "generations": 10},
        {"id": 2, "name": "Старт", "price": 499, "generations": 15},
        {"id": 3, "name": "Стандарт", "price": 1999, "generations": 30},
        {"id": 4, "name": "Премиум", "price": 2999, "generations": 60},
    ]

    buttons = [
        [InlineKeyboardButton(text=f"{pkg['name']} - {pkg['price']} руб.", callback_data=f"buy_{pkg['id']}")]
        for pkg in packages
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def profile_keyboard():
    """Клавиатура профиля"""
    buttons = [
        [InlineKeyboardButton(text="🔄 Обновить профиль", callback_data="profile_refresh")],
        [InlineKeyboardButton(text="💰 Пополнить генерации", callback_data="menu_buy")],
        [InlineKeyboardButton(text="⚙ Настройки", callback_data="menu_settings")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


PHOTO_FORMATS = {
    "1:1": "1x1",
    "3:4": "3x4",
    "9:16": "9x16",
    "16:9": "16x9"
}

def settings_keyboard():
    """Клавиатура выбора формата фото"""
    buttons = [
        [InlineKeyboardButton(text=format_option, callback_data=f"settings_{PHOTO_FORMATS[format_option]}")]
        for format_option in PHOTO_FORMATS.keys()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)



SUPPORT_USERNAME = "your_support_username"  # Укажите username службы поддержки

def support_keyboard():
    """Клавиатура поддержки"""
    buttons = [
        [InlineKeyboardButton(text="📞 Связаться с поддержкой", url=f"https://t.me/{SUPPORT_USERNAME}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def start_keyboard():
    """Клавиатура для выбора перед началом"""
    buttons = [
        [InlineKeyboardButton(text="🛒 Купить", callback_data="start_buy")],
        [InlineKeyboardButton(text="ℹ Инструкция", callback_data="start_instruction")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def pay_keyboard(payment_url):
    """Клавиатура для оплаты"""
    button = InlineKeyboardButton(text="💳 Оплатить", url=payment_url)
    return InlineKeyboardMarkup(inline_keyboard=[[button]])