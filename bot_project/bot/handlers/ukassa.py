# bot/handlers/ukassa.py

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, types
from bot.services.api_client import api_client
from bot.keyboards.inline import InlineKeyboardMarkup, InlineKeyboardButton, pay_keyboard
import logging

router = Router()


# 🔹 Машина состояний для ввода email
class PaymentState(StatesGroup):
    waiting_for_email = State()


@router.message(PaymentState.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    """Обрабатываем email пользователя"""
    email = message.text.strip()

    if "@" not in email or "." not in email:
        await message.answer("❌ Некорректный email. Пожалуйста, введите корректный email.")
        return

    # Сохраняем email в контексте состояния
    await state.update_data(email=email)

    try:
        # Получаем список пакетов из API
        packages = await api_client.get_package_types()
        if "error" in packages:
            await message.answer("❌ Ошибка при получении списка пакетов.")
            return

        # Формируем inline-клавиатуру с вариантами пакетов
        buttons = [
            [InlineKeyboardButton(text=f"📦 {pkg['name']} {pkg['total_generations']} генераций - {pkg['amount']}₽", callback_data=f"payment_{pkg['id']}")]
            for pkg in packages
        ]

        await message.answer(
            "💰 Выберите пакет генераций:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )
        await state.clear()

    except Exception as e:
        logging.error(f"Ошибка получения пакетов: {e}")
        await message.answer("❌ Ошибка при получении списка пакетов.")


@router.callback_query(lambda c: c.data.startswith("payment_"))
async def create_payment(callback: types.CallbackQuery, state: FSMContext):
    """Создание платежа в ЮKassa"""
    package_type_id = int(callback.data.split("_")[1])

    # Получаем email пользователя
    user_data = await state.get_data()
    email = user_data.get("email")

    if not email:
        respone  = await api_client.get_user_profile(callback.from_user.id)
        email = respone.get("email")

    if not email:
        await callback.message.edit_text("❌ Ошибка: Email не найден. Попробуйте заново.")
        return

    await callback.message.edit_text("⏳ Создаем платеж, подождите...")

    try:
        tg_user_id = callback.from_user.id
        message = await callback.message.answer("💳 Ожидаем ссылку на оплату...")

        # Передаем `message_id` в API при создании платежа
        response = await api_client.create_payment(
            user_id=tg_user_id,
            email=email,
            package_type_id=package_type_id,
            message_id=message.message_id,
            telegram_id=tg_user_id
        )

        payment_url = response.get("payment_url")

        if payment_url:
            await message.edit_text(
                f"✅ Оплата создана! Перейдите по ссылке:",
                reply_markup=pay_keyboard(payment_url)
            )
        else:
            await message.edit_text("❌ Ошибка при создании платежа.")
    except Exception as e:
        logging.error(f"Ошибка создания платежа: {e}")
        await callback.message.edit_text(f"❌ Ошибка: {e}")

    await callback.answer()

