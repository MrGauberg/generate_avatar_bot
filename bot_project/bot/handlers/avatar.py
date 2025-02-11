# bot/handlers/avatar.py

from aiogram import Router, types, Bot
from bot.services.api_client import api_client
from bot.config import Settings
from bot.keyboards.inline import gender_selection_keyboard
import tempfile
import os
import logging
import aiofiles
from asgiref.sync import sync_to_async

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
    temp_files = []  # Список временных файлов
    file_tuples = []  # Файлы в формате, ожидаемом API

    try:
        for i, photo_id in enumerate(user_photos[user_id]):
            temp_file_path = os.path.join(tempfile.gettempdir(), f"photo_{i}.jpg")

            # Скачиваем фото
            await bot.download(photo_id, destination=temp_file_path)
            temp_files.append(temp_file_path)

            # Читаем файл асинхронно перед отправкой
            async with aiofiles.open(temp_file_path, 'rb') as file:
                file_content = await file.read()
                file_name = os.path.basename(temp_file_path)
                file_tuples.append(('images', (file_name, file_content, 'image/jpeg')))

        # Отправляем файлы в API
        response = await api_client.upload_avatar(files=file_tuples, gender=gender)

        # Удаляем временные файлы после загрузки
        for temp_file in temp_files:
            await sync_to_async(os.remove)(temp_file)

        avatar_id = response.get("avatar_id")
        if avatar_id:
            await callback.message.edit_text(f"🎉 Аватар создан! ID: {avatar_id}")
        else:
            await callback.message.edit_text("❌ Ошибка при создании аватара.")

    except Exception as e:
        logging.error(f"Ошибка загрузки аватара: {e}")
        await callback.message.edit_text(f"❌ Ошибка: {e}")

    # Очищаем временные данные
    del user_photos[user_id]
    await callback.answer()
