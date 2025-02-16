# bot/handlers/avatar.py

from aiogram import Router, types, Bot
from bot.services.api_client import api_client
from bot.config import Settings
from bot.keyboards.inline import (
    add_avatar_keyboard,
    avatar_menu_keyboard,
    gender_selection_keyboard,
    get_avatar_slider_keyboard,
)
import tempfile
import os
import logging
import aiofiles
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from bot.utils.auth import require_authorization

from bot.services.redis_client import redis_client

router = Router()

MAX_PHOTOS = Settings.service.IMAGES_COUNT

# Храним загруженные фото временно (можно заменить на БД)
user_photos = {}
GENDER_CHOICES = {
    "avatar_gender_male": "male",
    "avatar_gender_female": "female",
    "avatar_gender_child": "child",
}


@router.callback_query(lambda c: c.data == "menu_create_avatar")
async def avatar_callback_handler(callback: types.CallbackQuery):
    """Обработка нажатия кнопки 'Создать аватар'"""
    await redis_client.clear_photos(callback.from_user.id)
    user_id = callback.from_user.id
    await redis_client.set_user_state(user_id, "waiting_for_photos")

    await callback.message.edit_text(
        f"📸 Отправьте мне {MAX_PHOTOS} фотографий для создания аватара.\n"
        "Фотографии должны быть разными и хорошо освещенными!"
    )
    await callback.answer()


@router.message(lambda message: message.photo)
async def handle_photo_upload(message: types.Message):
    """Обработка загруженных фотографий"""
    user_id = message.from_user.id

    user_state = await redis_client.get_user_state(user_id)

    if user_state != "waiting_for_photos":
        await message.answer("⚠ Сейчас загрузка фото не требуется. Начните создание аватара заново.")
        return
    
    photos = await redis_client.get_photos(user_id)
    if len(photos) >= MAX_PHOTOS:
        await message.answer("⚠ Вы уже загрузили достаточное количество фото!")
        return

    # Берем ТОЛЬКО самое большое фото
    largest_photo = message.photo[-1].file_id
    await redis_client.save_photo(user_id, largest_photo)

    photos = await redis_client.get_photos(user_id)
    uploaded_count = len(photos)

    if uploaded_count < MAX_PHOTOS:
        await message.answer(f"📷 Принято! Загружено {uploaded_count}/{MAX_PHOTOS} фото.")
    else:
        # Получаем список полов из API один раз
        genders = await api_client.get_avatar_genders()
        
        await redis_client.set_user_state(user_id, "waiting_for_gender")
        await message.answer(
            "✅ Все фото загружены!\nВыберите пол аватара:",
            reply_markup=gender_selection_keyboard(genders),
        )



@router.callback_query(lambda c: c.data.startswith("avatar_gender_"))
async def handle_gender_choice(callback: types.CallbackQuery, bot: Bot):
    """Обработка выбора пола"""
    user_id = callback.from_user.id

    # Получаем список полов из API
    genders = await api_client.get_avatar_genders()
    gender_id = int(callback.data.split("_")[-1])
    gender = genders.get(gender_id, "Неизвестный")

    photos = await redis_client.get_photos(user_id)

    if len(photos) < MAX_PHOTOS:
        await callback.message.edit_text(
            f"⚠ Пожалуйста, сначала загрузите {MAX_PHOTOS} фото!"
        )
        return

    await callback.message.edit_text("📤 Отправляем фото на сервер, подождите...")

    # Подготовка файлов для загрузки
    files = []
    temp_files = []  

    try:
        for i, photo_id in enumerate(photos):
            temp_file_path = os.path.join(tempfile.gettempdir(), f"photo_{i}.jpg")

            await bot.download(photo_id, destination=temp_file_path)
            temp_files.append(temp_file_path)

            async with aiofiles.open(temp_file_path, "rb") as temp_file:
                file_data = await temp_file.read()
                if file_data:
                    files.append(("images", (f"photo_{i}.jpg", file_data, "image/jpeg")))

        # Отправляем файлы в API
        response = await api_client.create_avatar(files=files, gender=gender_id, tg_user_id=user_id)
        avatar_id = response.get("avatar_id")

        if avatar_id:
            await redis_client.set_user_authorized(user_id, True)
            await callback.message.edit_text(f"🎉 Аватар создан! ID: {avatar_id}. Можем приступать к генерации фотографий")
        else:
            await callback.message.edit_text("❌ Ошибка при создании аватара.")

    except Exception as e:
        logging.error(f"Ошибка загрузки аватара: {e}")
        await callback.message.edit_text(f"❌ Ошибка: {e}")

    finally:
        for temp_file_path in temp_files:
            try:
                os.remove(temp_file_path)
            except Exception as e:
                logging.warning(f"Не удалось удалить файл {temp_file_path}: {e}")

        await redis_client.clear_photos(user_id)

    await callback.answer()




@router.message(lambda message: message.text == "🖼 Аватар")
@require_authorization
async def avatar_button_handler(message: types.Message):
    """Обработка кнопки 'Аватар'"""
    await message.answer(
        "👤 Здесь ты можешь выбрать человека, с лицом которого генерируются фотографии.",
        reply_markup=avatar_menu_keyboard(),
    )


@router.callback_query(lambda c: c.data == "avatar_select")
async def select_avatar_handler(callback: types.CallbackQuery):
    """Обработка выбора аватара (загрузка списка из API)"""
    await callback.message.edit_text("⏳ Загружаем список твоих аватаров...")

    try:
        avatars = await api_client.get_user_avatars(callback.from_user.id)
        if not avatars:
            await callback.message.edit_text(
                "❌ У тебя пока нет аватаров. Добавь новый!"
            )
            return

        await callback.message.edit_text(
            "Выбери аватар:", reply_markup=get_avatar_slider_keyboard(avatars)
        )
    except Exception as e:
        await callback.message.edit_text(
            f"❌ Ошибка при получении списка аватаров: {e}"
        )

    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("avatar_page_"))
async def avatar_pagination_handler(callback: types.CallbackQuery):
    """Переключение страниц аватаров"""
    page = int(callback.data.split("_")[2])
    avatars = await api_client.get_user_avatars(callback.from_user.id)

    await callback.message.edit_text(
        "Выбери аватар:", reply_markup=get_avatar_slider_keyboard(avatars, page)
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("avatar_select"))
async def activate_avatar_handler(callback: types.CallbackQuery):
    """Активация выбранного аватара"""
    avatar_id = int(callback.data.split("_")[2])
    avatar_name = callback.data.split("_")[3]

    try:
        response = await api_client.activate_avatar(avatar_id)
        if not response.get("error"):
            await callback.message.edit_text(
                f"Модель {avatar_name} выбрана, теперь генерируем фотографии с этой моделью✅"
            )
        else:
            await callback.message.edit_text("❌ Ошибка при выборе аватара.")
    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка: {e}")

    await callback.answer()


@router.callback_query(lambda c: c.data == "avatar_menu")
async def return_to_avatar_menu(callback: types.CallbackQuery):
    """Возвращение в меню аватаров"""
    await callback.message.edit_text(
        "👤 Здесь ты можешь выбрать человека, с лицом которого генерируются фотографии.",
        reply_markup=avatar_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "avatar_add")
async def add_avatar_handler(callback: types.CallbackQuery, state: FSMContext):
    """Проверка доступных слотов и покупка слота"""
    tg_user_id = callback.from_user.id
    response = await api_client.check_avatar_slots(tg_user_id)

    if response.get("can_add_avatar"):
        await callback.message.edit_text(
            "📸 У вас есть свободный слот! Приступаем к созданию аватара."
        )
        await avatar_callback_handler(callback)
    else:
        price = await api_client.get_avatar_price()
        await callback.message.edit_text(
            f"🔹 У вас нет свободных слотов для нового аватара.\n"
            f"💰 **Стоимость добавления слота: {price:.2f}₽**\n\n"
            "Выберите действие:",
            reply_markup=add_avatar_keyboard(),
        )
    await callback.answer()


@router.callback_query(lambda c: c.data == "avatar_buy")
async def buy_avatar_handler(callback: types.CallbackQuery):
    """Создание платежа для добавления слота аватара"""
    await callback.message.edit_text("⏳ Создаем платеж, подождите...")

    try:
        tg_user_id = callback.from_user.id
        data = {
            "telegram_id": tg_user_id,
            "message_id": callback.message.message_id,
        }
        response = await api_client.buy_avatart_slot(data)

        payment_url = response.get("payment_url")

        if payment_url:
            await callback.message.edit_text(
                f"✅ Оплата создана! Перейдите по ссылке:",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="💳 Оплатить", url=payment_url)]
                    ]
                ),
            )
        else:
            await callback.message.edit_text("❌ Ошибка при создании платежа.")
    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка: {e}")

    await callback.answer()
