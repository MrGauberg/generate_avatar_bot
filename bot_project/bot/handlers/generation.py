# bot/handlers/generation.py

from aiogram import Router, types
from bot.services.api_client import api_client
from bot.keyboards.inline import get_categories_keyboard, get_styles_keyboard

router = Router()


@router.callback_query(lambda c: c.data == "menu_generate_images")
async def generate_menu_callback(callback: types.CallbackQuery):
    """Обработка нажатия кнопки 'Генерация изображений'"""
    await callback.message.edit_text("📂 Выберите категорию:", reply_markup=await get_category_buttons())
    await callback.answer()


async def get_category_buttons():
    """Создает inline-кнопки с категориями"""
    categories = await api_client.get_categories_list()
    return get_categories_keyboard(categories)


async def get_style_buttons(category_id):
    """Создает inline-кнопки со стилями для выбранной категории"""
    styles = await api_client.get_styles_list()
    return get_styles_keyboard(styles, category_id)


@router.callback_query(lambda c: c.data.startswith("category_"))
async def category_selected_callback(callback: types.CallbackQuery):
    """Обработка выбора категории"""
    category_id = int(callback.data.split("_")[1])
    keyboard = await get_style_buttons(category_id)
    await callback.message.edit_text("🎨 Выберите стиль:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("generate_"))
async def generate_image_callback(callback: types.CallbackQuery):
    """Обработка выбора стиля и генерация изображения"""
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
