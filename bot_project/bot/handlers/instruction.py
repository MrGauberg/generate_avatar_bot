
# bot/handlers/instruction.py

from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


@router.callback_query(lambda c: c.data == "start_instruction")
async def instruction_step_1(callback: types.CallbackQuery):
    """Первый шаг инструкции - описание бота"""
    await callback.message.edit_text(
        "ℹ **Описание бота**\n\n"
        "Этот бот позволяет создавать аватар и генерировать изображения.\n"
        "📸 Вы загружаете 10 фото, и бот создает уникальный аватар.\n"
        "🎨 Затем вы можете генерировать фото в разных стилях.\n\n"
        "✅ **Все понял!** → Подробнее про форматы фото",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Все понял!", callback_data="instruction_photo_format")]]
        )
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "instruction_photo_format")
async def instruction_step_2(callback: types.CallbackQuery):
    """Второй шаг инструкции - форматы фото"""
    await callback.message.edit_text(
        "📏 **Формат фотографий**\n\n"
        "Чтобы создать аватар, загрузите 10 фотографий:\n"
        "- **Разные позы**\n"
        "- **Хорошее освещение**\n"
        "- **Без очков и головных уборов**\n\n"
        "➡ **Дальше!** → Описание двух режимов",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Дальше!", callback_data="instruction_modes")]]
        )
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "instruction_modes")
async def instruction_step_3(callback: types.CallbackQuery):
    """Третий шаг инструкции - два режима"""
    await callback.message.edit_text(
        "⚡ **Два режима работы**\n\n"
        "1️⃣ **Обычный режим** - Выбирайте стили и категории, чтобы генерировать фото.\n"
        "2️⃣ **Режим Бога** - Включите этот режим и просто опишите, что хотите увидеть.\n\n"
        "💰 **А сколько стоит?**",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="А сколько стоит?", callback_data="instruction_prices")]]
        )
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "instruction_prices")
async def instruction_step_4(callback: types.CallbackQuery):
    """Четвертый шаг инструкции - стоимость"""
    await callback.message.edit_text(
        "💰 **Стоимость пакетов**\n\n"
        "📦 **Пробный** - 199₽ (10 генераций)\n"
        "📦 **Старт** - 499₽ (15 генераций)\n"
        "📦 **Стандарт** - 1999₽ (30 генераций)\n"
        "📦 **Премиум** - 2999₽ (60 генераций)\n\n"
        "✅ **Купить** → Перед оплатой ознакомьтесь с соглашением",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Купить", callback_data="start_buy")]]
        )
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "start_buy")
async def confirm_terms(callback: types.CallbackQuery):
    """Пользователь должен подтвердить соглашение перед оплатой"""
    await callback.message.edit_text(
        "📜 **Пользовательское соглашение**\n\n"
        "Перед оплатой ознакомьтесь с условиями:\n"
        "[Ссылка на соглашение](https://example.com/terms)\n\n"
        "✅ Подтверждаю",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="✅ Подтвердить", callback_data="start_payment_email")]]
        )
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "start_payment_email")
async def request_email(callback: types.CallbackQuery):
    """Запрос email перед оплатой"""
    await callback.message.edit_text(
        "📧 Введите ваш email для получения чека и подтверждения оплаты:"
    )
    await callback.answer()
