# bot/keyboards/inline.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import Settings


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



def profile_keyboard():
    """Клавиатура профиля"""
    buttons = [
        [InlineKeyboardButton(text="🔄 Обновить профиль", callback_data="profile_refresh")],
        [InlineKeyboardButton(text="💰 Пополнить генерации", callback_data="menu_buy")],
        [InlineKeyboardButton(text="⚙ Настройки", callback_data="menu_settings")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)



def support_keyboard():
    """Клавиатура поддержки"""
    buttons = [
        [InlineKeyboardButton(text="📞 Связаться с поддержкой", url=f"https://t.me/{Settings.user.tg_user_name}")]
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


def avatar_menu_keyboard():
    """Клавиатура выбора аватара"""
    buttons = [
        [InlineKeyboardButton(text="🖼 Выбрать аватар", callback_data="avatar_select")],
        [InlineKeyboardButton(text="➕ Добавить аватар", callback_data="avatar_add")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_avatar_slider_keyboard(avatars, page=0):
    """Создает inline-клавиатуру с аватарами (слайдер по 3 штуки)"""
    buttons = []
    avatars_per_page = 3
    start_index = page * avatars_per_page
    end_index = start_index + avatars_per_page
    paged_avatars = avatars[start_index:end_index]

    for avatar in paged_avatars:
        active = " ✅" if avatar.get("is_active", False) else ""
        avatar_id = f" № {avatar.get('id')}" if avatar.get("id") else ""
        print(avatar)
        buttons.append([InlineKeyboardButton(text=f"🖼 {avatar['name']}{avatar_id}{active}", callback_data=f"avatar_select_{avatar['id']}_{avatar['name']}")])

    nav_buttons = []
    if start_index > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅ Назад", callback_data=f"avatar_page_{page - 1}"))
    else:
        if len(avatars) > avatars_per_page:
            nav_buttons.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
    if len(avatars) > avatars_per_page:
        nav_buttons.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
    if end_index < len(avatars):
        nav_buttons.append(InlineKeyboardButton(text="Вперед ➡", callback_data=f"avatar_page_{page + 1}"))
    else:
        if len(avatars) > avatars_per_page:
            nav_buttons.append(InlineKeyboardButton(text=" ", callback_data="ignore"))

    if nav_buttons:
        buttons.append(nav_buttons)

    buttons.append([InlineKeyboardButton(text="🔙 В меню", callback_data="avatar_menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)



def add_avatar_keyboard():
    """Клавиатура для покупки нового аватара"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Купить", callback_data="avatar_buy")],
            [InlineKeyboardButton(text="📞 Поддержка", callback_data="menu_support")]
        ]
    )

def get_packages_keyboard():
    """Клавиатура с кнопкой 'Выберите пакет'"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Выберите пакет", callback_data="choose_package")]
        ]
    )


PHOTO_FORMATS = {
    "1:1": "1:1",
    "3:4": "3:4",
    "9:16": "9:16",
    "16:9": "16:9"
}

def settings_menu_keyboard():
    """Клавиатура настроек"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📏 Формат фото", callback_data="settings_photo_format")]
        ]
    )

def photo_format_keyboard():
    """Клавиатура выбора формата фото"""
    buttons = [
        [InlineKeyboardButton(text=format_option, callback_data=f"set_photo_format_{PHOTO_FORMATS[format_option]}")]
        for format_option in PHOTO_FORMATS.keys()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def god_mode_keyboard(is_enabled: bool):
    """Клавиатура включения/выключения режима 'Бога'"""
    buttons = [
        [InlineKeyboardButton(
            text="❌ Выключить режим Бога" if is_enabled else "🔮 Включить режим Бога",
            callback_data="godmode_toggle"
        )],
        [InlineKeyboardButton(text="ℹ Инструкция", callback_data="godmode_instruction")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def god_mode_instruction_keyboard():
    """Клавиатура для инструкции режима Бога"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="godmode_menu")]]
    )



def get_categories_slider(categories, page=0):
    """Создает inline-клавиатуру с категориями (слайдер по 3 штуки)"""
    categories.insert(0, {"id": 0, "name": "Без категории"}) 

    buttons = []
    categories_per_page = 3
    start_index = page * categories_per_page
    end_index = start_index + categories_per_page
    paged_categories = categories[start_index:end_index]

    for category in paged_categories:
        category_name = category["name"]
        category_id = category["id"]
        buttons.append([
            InlineKeyboardButton(text=category_name, callback_data=f"category_selected_{category_id}_{category_name}")
        ])

    nav_buttons = []
    if start_index > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅ Назад", callback_data=f"category_page_{page - 1}"))
    else:
        if len(categories) > categories_per_page:
            nav_buttons.append(InlineKeyboardButton(text=" ", callback_data="ignore"))

    if len(categories) > categories_per_page:
        nav_buttons.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
    if end_index < len(categories):
        nav_buttons.append(InlineKeyboardButton(text="Вперед ➡", callback_data=f"category_page_{page + 1}"))
    else:
        if len(categories) > categories_per_page:
            nav_buttons.append(InlineKeyboardButton(text=" ", callback_data="ignore"))

    if nav_buttons:
        buttons.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_styles_slider(styles, page=0):
    """Создает inline-клавиатуру с слайдером стилей (по 3 штуки)"""
    buttons = []
    styles_per_page = 3
    start_index = page * styles_per_page
    end_index = start_index + styles_per_page
    paged_styles = styles[start_index:end_index]
    category_id = paged_styles[0]["category"]

    for style in paged_styles:
        buttons.append([InlineKeyboardButton(text=style["name"], callback_data=f"style_{style['id']}")])

    nav_buttons = []
    if start_index > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅ Назад", callback_data=f"style_page_{page - 1}_{category_id}"))
    else:
        if len(styles) > styles_per_page:
            nav_buttons.append(InlineKeyboardButton(text=" ", callback_data="ignore"))

    if len(styles) > styles_per_page:
        nav_buttons.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
        
    if end_index < len(styles):
        nav_buttons.append(InlineKeyboardButton(text="Вперед ➡", callback_data=f"style_page_{page + 1}_{category_id}"))
    else:
        if len(styles) > styles_per_page:
            nav_buttons.append(InlineKeyboardButton(text=" ", callback_data="ignore"))

    if nav_buttons:
        buttons.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)
