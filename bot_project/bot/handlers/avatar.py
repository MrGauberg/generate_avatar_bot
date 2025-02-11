# bot/handlers/avatar.py

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.services.api_client import api_client

router = Router()

# Хранение загруженных фото временно в памяти (можно заменить на БД)
user_photos = {}

GENDER_CHOICES = {
    "Мужчина": "male",
    "Женщина": "female",
    "Ребенок": "child"
}

async def request_gender_choice(message: types.Message):
    """Запрос выбора пола после загрузки фото"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужчина")],
            [KeyboardButton(text="Женщина")],
            [KeyboardButton(text="Ребенок")]
        ],
        resize_keyboard=True
    )
    await message.answer("Теперь выбери пол аватара:", reply_markup=keyboard)


@router.message(Command("avatar"))
async def avatar_command_handler(message: types.Message):
    """Команда для загрузки аватара"""
    await message.answer(
        "📸 Отправь мне 10 фотографий для создания аватара. "
        "Они должны быть разными и хорошо освещенными!"
    )
    user_photos[message.from_user.id] = []


@router.message(lambda message: message.photo)
async def handle_photo_upload(message: types.Message):
    """Обработка загруженных фотографий"""
    user_id = message.from_user.id

    if user_id not in user_photos:
        user_photos[user_id] = []

    user_photos[user_id].append(message.photo[-1].file_id)

    if len(user_photos[user_id]) < 10:
        await message.answer(f"📷 Принято! Загружено {len(user_photos[user_id])}/10 фото.")
    else:
        await message.answer("✅ Все фото загружены!")
        await request_gender_choice(message)


@router.message(lambda message: message.text in GENDER_CHOICES)
async def handle_gender_choice(message: types.Message):
    """Обработка выбора пола"""
    user_id = message.from_user.id
    gender = GENDER_CHOICES[message.text]

    if user_id not in user_photos or len(user_photos[user_id]) < 10:
        await message.answer("⚠ Пожалуйста, сначала загрузите 10 фото!")
        return

    await message.answer("📤 Отправляем фото на сервер, подождите...")

    # Подготавливаем файлы для загрузки
    files = [("images", (f"photo_{i}.jpg", await message.bot.download_file_by_id(photo_id), "image/jpeg"))
             for i, photo_id in enumerate(user_photos[user_id])]

    try:
        response = await api_client.upload_avatar(files=files, gender=gender)
        avatar_id = response.get("avatar_id")
        if avatar_id:
            await message.answer(f"🎉 Аватар создан! ID: {avatar_id}")
        else:
            await message.answer("❌ Ошибка при создании аватара.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

    # Очищаем временные данные
    del user_photos[user_id]
