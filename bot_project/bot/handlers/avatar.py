# bot/handlers/avatar.py

from aiogram import Router, types, Bot
from bot.services.api_client import api_client
from bot.config import Settings
from bot.keyboards.inline import gender_selection_keyboard
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
        response = await api_client.upload_avatar(files=files, gender=gender)
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
