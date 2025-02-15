
# bot/handlers/instruction.py

from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from bot.services.api_client import api_client
from aiogram.fsm.context import FSMContext

from bot.handlers.ukassa import PaymentState

router = Router()

logging.basicConfig(level=logging.INFO)

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
    """Динамическое формирование списка пакетов генераций"""
    await callback.message.edit_text("⏳ Загружаем актуальные пакеты...")

    try:
        # Получаем список пакетов из API
        packages = await api_client.get_package_types()
        if "error" in packages:
            await callback.message.edit_text("❌ Ошибка при получении списка пакетов.")
            return

        # Формируем текст с пакетами
        packages_text = "\n".join(
            [f"📦 **{pkg['name']}** - {pkg['amount']}₽ ({pkg['total_generations']} генераций)" for pkg in packages]
        )

        await callback.message.edit_text(
            f"💰 **Стоимость пакетов**\n\n{packages_text}\n\n✅ **Купить** → Перед оплатой ознакомьтесь с соглашением",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="Купить", callback_data="start_buy")]]
            ),
            parse_mode="Markdown"
        )

    except Exception as e:
        logging.error(f"Ошибка получения пакетов: {e}")
        await callback.message.edit_text("❌ Ошибка при получении списка пакетов.")

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
async def request_email(callback: types.CallbackQuery, state: FSMContext):
    """Запрос email перед оплатой"""
    await callback.message.edit_text(
        "📧 Введите ваш email для подтверждения оплаты:"
    )
    await state.set_state(PaymentState.waiting_for_email)
    await callback.answer()
