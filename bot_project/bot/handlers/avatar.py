# bot/handlers/avatar.py

from aiogram import Router, types, Bot
from bot.services.api_client import api_client
from bot.config import Settings
from bot.keyboards.inline import add_avatar_keyboard, avatar_menu_keyboard, gender_selection_keyboard, get_avatar_slider_keyboard
import tempfile
import os
import logging
import aiofiles

router = Router()

MAX_PHOTOS = Settings.service.AVATAR_IMAGES_COUNT

# Храним загруженные фото временно (можно заменить на БД)
user_photos = {}
GENDER_CHOICES = {
    "avatar_gender_male": "male",
    "avatar_gender_female": "female",
    "avatar_gender_child": "child"
}


@router.callback_query(lambda c: c.data == "menu_create_avatar")
async def avatar_callback_handler(callback: types.CallbackQuery):
    """Обработка нажатия кнопки 'Создать аватар'"""
    await callback.message.edit_text(
        f"📸 Отправьте мне {MAX_PHOTOS} фотографий для создания аватара.\n"
        "Фотографии должны быть разными и хорошо освещенными!"
    )
    user_photos[callback.from_user.id] = []
    await callback.answer()


@router.message(lambda message: message.photo)
async def handle_photo_upload(message: types.Message):
    """Обработка загруженных фотографий"""
    user_id = message.from_user.id

    if user_id not in user_photos:
        user_photos[user_id] = []

    user_photos[user_id].append(message.photo[-1].file_id)

    if len(user_photos[user_id]) < MAX_PHOTOS:
        await message.answer(f"📷 Принято! Загружено {len(user_photos[user_id])}/{MAX_PHOTOS} фото.")
    else:
        await message.answer("✅ Все фото загружены!\nВыберите пол аватара:", reply_markup=gender_selection_keyboard())


@router.callback_query(lambda c: c.data in GENDER_CHOICES)
async def handle_gender_choice(callback: types.CallbackQuery, bot: Bot):
    """Обработка выбора пола"""
    user_id = callback.from_user.id
    gender = GENDER_CHOICES[callback.data]

    if user_id not in user_photos or len(user_photos[user_id]) < MAX_PHOTOS:
        await callback.message.edit_text(f"⚠ Пожалуйста, сначала загрузите {MAX_PHOTOS} фото!")
        return

    await callback.message.edit_text("📤 Отправляем фото на сервер, подождите...")

    # Подготовка файлов для загрузки
    files = []
    temp_files = []  # Список для хранения путей временных файлов

    try:
        for i, photo_id in enumerate(user_photos[user_id]):
            temp_file_path = os.path.join(tempfile.gettempdir(), f"photo_{i}.jpg")

            # Скачиваем фото В ФАЙЛ, а не в поток
            await bot.download(photo_id, destination=temp_file_path)

            temp_files.append(temp_file_path)

            # Читаем содержимое и добавляем в список файлов для API
            async with aiofiles.open(temp_file_path, "rb") as temp_file:
                file_data = await temp_file.read()
                if file_data:
                    files.append(("images", (f"photo_{i}.jpg", file_data, "image/jpeg")))

        print("Файлы, отправляемые в API:", len(files))

        # Отправляем файлы в API
        response = await api_client.create_avatar(files=files, gender=gender)
        avatar_id = response.get("avatar_id")

        if avatar_id:
            await callback.message.edit_text(f"🎉 Аватар создан! ID: {avatar_id}")
        else:
            await callback.message.edit_text("❌ Ошибка при создании аватара.")
    except Exception as e:
        logging.error(f"Ошибка загрузки аватара: {e}")
        await callback.message.edit_text(f"❌ Ошибка: {e}")
    finally:
        # Удаляем временные файлы
        for temp_file_path in temp_files:
            try:
                os.remove(temp_file_path)
            except Exception as e:
                logging.warning(f"Не удалось удалить файл {temp_file_path}: {e}")

    # Очищаем временные данные
    del user_photos[user_id]
    await callback.answer()


@router.message(lambda message: message.text == "🖼 Аватар")
async def avatar_button_handler(message: types.Message):
    """Обработка кнопки 'Аватар'"""
    await message.answer(
        "👤 Здесь ты можешь выбрать человека, с лицом которого генерируются фотографии.",
        reply_markup=avatar_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == "avatar_select")
async def select_avatar_handler(callback: types.CallbackQuery):
    """Обработка выбора аватара (загрузка списка из API)"""
    await callback.message.edit_text("⏳ Загружаем список твоих аватаров...")

    try:
        avatars = await api_client.get_user_avatars(callback.from_user.id)
        if not avatars:
            await callback.message.edit_text("❌ У тебя пока нет аватаров. Добавь новый!")
            return

        await callback.message.edit_text("Выбери аватар:", reply_markup=get_avatar_slider_keyboard(avatars))
    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка при получении списка аватаров: {e}")

    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("avatar_page_"))
async def avatar_pagination_handler(callback: types.CallbackQuery):
    """Переключение страниц аватаров"""
    page = int(callback.data.split("_")[2])
    avatars = await api_client.get_user_avatars(callback.from_user.id)

    await callback.message.edit_text("Выбери аватар:", reply_markup=get_avatar_slider_keyboard(avatars, page))
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("avatar_"))
async def activate_avatar_handler(callback: types.CallbackQuery):
    """Активация выбранного аватара"""
    avatar_id = int(callback.data.split("_")[1])

    try:
        response = await api_client.activate_avatar(avatar_id)
        if response.get("success"):
            await callback.message.edit_text(f"✅ Аватар ID {avatar_id} выбран!")
        else:
            await callback.message.edit_text("❌ Ошибка при выборе аватара.")
    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка: {e}")

    await callback.answer()


@router.callback_query(lambda c: c.data == "avatar_add")
async def add_avatar_handler(callback: types.CallbackQuery):
    """Обработка добавления нового аватара"""
    await callback.message.edit_text(
        "🔹 Ты можешь иметь сразу несколько аватаров и выбирать любой из них для генерации изображений.\n\n"
        "💰 **Стоимость добавления нового аватара: 490₽**\n\n"
        "Выбери действие:",
        reply_markup=add_avatar_keyboard()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "avatar_buy")
async def buy_avatar_handler(callback: types.CallbackQuery):
    """Создание платежа для добавления аватара"""
    await callback.message.edit_text("⏳ Создаем платеж на 490₽, подождите...")

    try:
        tg_user_id = callback.from_user.id
        response = await api_client.create_payment(
            user_id=tg_user_id,
            email="avatar_payment@bot.com",
            package_type_id=5,  # ID пакета для покупки аватара (нужно настроить в API)
            message_id=callback.message.message_id,
            telegram_id=tg_user_id
        )

        payment_url = response.get("payment_url")

        if payment_url:
            await callback.message.edit_text(
                f"✅ Оплата создана! Перейдите по ссылке:",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="💳 Оплатить", url=payment_url)]]
                )
            )
        else:
            await callback.message.edit_text("❌ Ошибка при создании платежа.")
    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка: {e}")

    await callback.answer()
