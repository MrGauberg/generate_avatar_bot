# bot/handlers/payments.py

from aiogram import Router, types
from bot.services.api_client import api_client
from bot.keyboards.inline import get_payment_keyboard, pay_keyboard

router = Router()


@router.callback_query(lambda c: c.data == "menu_buy")
async def buy_menu_callback(callback: types.CallbackQuery):
    """Обработка нажатия кнопки 'Купить генерации'"""
    await callback.message.edit_text("💰 Выберите пакет генераций:", reply_markup=get_payment_keyboard())
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("buy_"))
async def handle_payment_callback(callback: types.CallbackQuery):
    """Обработка выбора пакета и создание платежа"""
    package_id = int(callback.data.split("_")[1])

    await callback.message.edit_text("⏳ Создаем платеж, подождите...")

    try:
        response = await api_client.purchase_generation_package(package_id)
        payment_url = response.get("payment_url")

        if payment_url:
            await callback.message.answer(
                "💳 **Оплатить сейчас:**",
                reply_markup=pay_keyboard(payment_url)
            )
        else:
            await callback.message.edit_text("❌ Ошибка при создании платежа.")
    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка: {e}")

    await callback.answer()

