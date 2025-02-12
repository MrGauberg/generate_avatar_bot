# bot/handlers/ukassa.py

from aiogram import Router, types

router = Router()


@router.callback_query(lambda c: c.data == "start_payment_email")
async def request_email(callback: types.CallbackQuery):
    """Запрос email перед оплатой"""
    await callback.message.edit_text(
        "📧 Введите ваш email для получения чека и подтверждения оплаты:"
    )
    await callback.answer()