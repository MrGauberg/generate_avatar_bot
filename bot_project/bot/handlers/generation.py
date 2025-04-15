from aiogram import Router, types
from bot.services.api_client import api_client
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards.inline import get_categories_keyboard, get_styles_keyboard
from bot.keyboards.inline import get_packages_keyboard
from bot.utils.auth import require_authorization

router = Router()


@router.message(lambda message: message.text == "💰 Генерации")
@router.callback_query(lambda c: c.data == "back_to_generations")
@require_authorization
async def generations_button_handler(event: types.Message | types.CallbackQuery):
    """Обработка кнопки 'Генерации'"""

    if isinstance(event, types.Message):
        message = event
        is_callback = False
    else:
        message = event.message
        is_callback = True

    user_id = event.from_user.id


    try:
        user_packages = await api_client.get_user_packages(user_id)

        if not isinstance(user_packages, list):
            await message.answer("❌ Ошибка при получении данных о генерациях.")
            return

        if not user_packages:
            if is_callback:
                await message.edit_text("❌ У вас нет активных пакетов генераций.", reply_markup=get_packages_keyboard())
            else:
                await event.answer("❌ У вас нет активных пакетов генераций.", reply_markup=get_packages_keyboard())
            return

        packages_text = "\n".join(
            [f"📦 **{pkg.get('package_name', 'Неизвестный пакет')}** — Осталось {pkg.get('generations_remains', 0)} генераций"
             for pkg in user_packages]
        )

        total_generations = sum(pkg.get("generations_remains", 0) for pkg in user_packages)

        text = (
            f"💰 **Ваши генерации**\n\n"
            f"📊 Общее количество доступных генераций: **{total_generations}**\n\n"
            f"{packages_text}\n\n"
            "🔹 Если генерации закончились, выберите новый пакет ниже:"
        )

        if is_callback:
            await message.edit_text(text, reply_markup=get_packages_keyboard())
        else:
            await message.answer(text, reply_markup=get_packages_keyboard())

    except Exception as e:
        await message.answer(f"❌ Ошибка при получении данных: {e}")




@router.callback_query(lambda c: c.data == "back_to_generations")
async def back_to_generations_handler(callback: types.CallbackQuery):
    """Возвращение к информации о генерациях"""
    await generations_button_handler(callback)
    await callback.answer()



@router.callback_query(lambda c: c.data == "menu_generate_images")
async def generate_menu_callback(callback: types.CallbackQuery):
    """Обработка нажатия кнопки 'Генерация изображений'"""
    await callback.message.edit_text("📂 Выберите категорию:", reply_markup=await get_category_buttons())
    await callback.answer()


async def get_category_buttons():
    """Создает inline-кнопки с категориями"""
    categories = await api_client.get_categories_list()
    return get_categories_keyboard(categories)


async def get_style_buttons(category_id, user_id):
    """Создает inline-кнопки со стилями для выбранной категории"""
    styles = await api_client.get_styles_list(user_id=user_id)
    return get_styles_keyboard(styles, category_id)


@router.callback_query(lambda c: c.data.startswith("generate_"))
async def generate_image_callback(callback: types.CallbackQuery):
    """Обработка выбора стиля и генерация изображения"""
    style_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    await callback.message.edit_text("⏳ Генерируем изображение, подождите...")

    try:
        response = await api_client.generate_user_image(prompt="", user_id=user_id)
        image_url = response.get("image_url")

        if image_url:
            await callback.message.answer_photo(photo=image_url, caption="✨ Сгенерированное изображение!")
        else:
            await callback.message.answer("❌ Ошибка генерации изображения.")
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка: {e}")

    await callback.answer()


@router.callback_query(lambda c: c.data == "choose_package")
async def choose_package_handler(callback: types.CallbackQuery):
    """Вывод списка пакетов для покупки"""
    await callback.message.edit_text("⏳ Загружаем доступные пакеты...")

    try:
        packages = await api_client.get_package_types()
        if not packages:
            await callback.message.edit_text("❌ Ошибка при получении списка пакетов.")
            return

        buttons = [
            [InlineKeyboardButton(text=f"📦 {pkg['name']} {pkg['total_generations']} генераций - {pkg['amount']}₽", callback_data=f"payment_{pkg['id']}")]
            for pkg in packages
        ]
        buttons.append([InlineKeyboardButton(text="📞 Поддержка", callback_data="menu_support")])
        buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_generations")])

        await callback.message.edit_text(
            "💰 **Выберите пакет для покупки:**",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            
        )

    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка при получении пакетов: {e}")

    await callback.answer()