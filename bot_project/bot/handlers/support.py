# bot/handlers/support.py

from aiogram import Router, types
from bot.keyboards.inline import support_keyboard

router = Router()


@router.message(lambda message: message.text == "📞 Поддержка")
async def support_message_handler(message: types.Message):
    """Обработка нажатия кнопки '📞 Поддержка' в главном меню"""
    support_text = (
        "📞 **Поддержка**\n\n"
        "Если у вас возникли вопросы или проблемы, нажмите кнопку ниже, чтобы связаться с нами:"
    )

    await message.answer(support_text, reply_markup=support_keyboard())


@router.callback_query(lambda c: c.data == "menu_support")
async def support_callback_handler(callback: types.CallbackQuery):
    """Обработка нажатия inline-кнопки 'Поддержка'"""
    support_text = (
        "📞 **Поддержка**\n\n"
        "Если у вас возникли вопросы или проблемы, нажмите кнопку ниже, чтобы связаться с нами:"
    )

    await callback.message.edit_text(support_text, reply_markup=support_keyboard())
    await callback.answer()
