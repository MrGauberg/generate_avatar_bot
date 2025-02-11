# bot/handlers/payments.py

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.services.api_client import api_client

router = Router()


async def get_payment_keyboard():
    """Создает клавиатуру с вариантами пакетов генераций"""
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


@router.message(Command("buy"))
async def buy_command_handler(message: types.Message):
    """Команда /buy для покупки пакетов генераций"""
    keyboard = await get_payment_keyboard()
    await message.answer("💰 Выберите пакет генераций:", reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("buy_"))
async def handle_payment(callback_query: types.CallbackQuery):
    """Обработка выбора пакета и создание платежа"""
    package_id = callback_query.data.split("_")[1]
    user_id = callback_query.from_user.id

    await callback_query.message.edit_text("⏳ Создаем платеж, подождите...")

    try:
        response = await api_client.purchase_generation_package(int(package_id))
        payment_url = response.get("payment_url")

        if payment_url:
            await callback_query.message.edit_text(
                f"✅ Оплата создана!\n\nПерейдите по ссылке для оплаты: [Оплатить]({payment_url})",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
        else:
            await callback_query.message.edit_text("❌ Ошибка при создании платежа.")
    except Exception as e:
        await callback_query.message.edit_text(f"❌ Ошибка: {e}")
