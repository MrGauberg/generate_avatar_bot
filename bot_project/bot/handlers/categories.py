# bot/handlers/categories.py

from aiogram import Router, types
from bot.services.api_client import api_client
from bot.keyboards.inline import get_categories_slider, get_styles_slider
from bot.utils.auth import require_authorization

router = Router()


@router.message(lambda message: message.text == "🎨 Стили")
@require_authorization
async def styles_button_handler(message: types.Message):
    """Обработка кнопки 'Стили'"""
    categories = await api_client.get_categories_list()
    await message.answer("📂 Выберите категорию:", reply_markup=get_categories_slider(categories))


@router.callback_query(lambda c: c.data.startswith("category_selected_"))
async def category_selected(callback: types.CallbackQuery):
    """Обработка выбора категории"""
    category_id = callback.data.split("_")[2]
    category_id = None if category_id == "0" else int(category_id)
    category_name = callback.data.split("_")[3]

    styles = await api_client.get_styles_list(category_id)

    await callback.message.edit_text(
        f"📂 **Категория: {category_name}**\n\nВыбери стиль и получи 2 фото:",
        reply_markup=get_styles_slider(styles)
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("category_page_"))
async def category_pagination_handler(callback: types.CallbackQuery):
    """Переключение страниц категорий"""
    page = int(callback.data.split("_")[2])
    categories = await api_client.get_categories_list()
    await callback.message.edit_text("📂 Выберите категорию:", reply_markup=get_categories_slider(categories, page))
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("style_page_"))
async def style_pagination_handler(callback: types.CallbackQuery):
    """Переключение страниц стилей"""
    page = int(callback.data.split("_")[2])
    category_id = int(callback.data.split("_")[3])
    styles = await api_client.get_styles_list(category_id)
    await callback.message.edit_text("📂 Выберите стиль и получите 2 фото:", reply_markup=get_styles_slider(styles, page))
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("style_"))
async def style_selected(callback: types.CallbackQuery):
    """Обработка выбора стиля"""
    style_id = int(callback.data.split("_")[1])

    await callback.message.edit_text("⏳ Генерируем изображение, подождите...")

    try:
        response = await api_client.generate_user_image(prompt="", model_id=style_id)
        image_url = response.get("image_url")

        if image_url:
            await callback.message.answer_photo(photo=image_url, caption="✨ Сгенерированное изображение!")
        else:
            await callback.message.answer("❌ Ошибка генерации изображения.")
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка: {e}")

    await callback.answer()


@router.callback_query(lambda c: c.data == "back_to_categories")
async def back_to_categories_handler(callback: types.CallbackQuery):
    """Возвращение к списку категорий"""
    categories = await api_client.get_categories_list()
    await callback.message.edit_text("📂 Выберите категорию:", reply_markup=get_categories_slider(categories))
    await callback.answer()

