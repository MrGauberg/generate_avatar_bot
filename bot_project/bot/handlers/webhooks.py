from aiohttp import web
from aiogram import Bot
from bot.config import Settings
import logging

from bot.services.redis_client import redis_client
from bot.keyboards.inline import get_packages_keyboard
from bot.keyboards.reply import main_menu_keyboard
from aiogram.types import InputMediaPhoto


bot = Bot(token=Settings.bot.TOKEN)

IMAGES_COUNT = Settings.service.IMAGES_COUNT



async def handle_payment_webhook(request):
    """Обработчик вебхука для подтверждения платежа"""
    try:
        data = await request.json()
        user_id = data.get("user_id")
        message_id = data.get("message_id")
        payment_type = data.get("payment_type")
        total_generations = data.get("total_generations")

        if not user_id or not message_id:
            return web.json_response({"error": "Missing user_id or message_id"}, status=400)

        # Очищаем старые загруженные фото в Redis
        await redis_client.clear_photos(user_id)
        await redis_client.set_user_state(user_id, "waiting_for_photos")

        # Отправляем сообщение пользователю после успешной оплаты
        if payment_type == "avatar":
            await bot.edit_message_text(
                f"✅ Оплата прошла успешно!\nТеперь отправьте {IMAGES_COUNT} фото для создания аватара.",
                chat_id=user_id,
                message_id=message_id
            )
        elif payment_type == "package":
            await bot.edit_message_text(
                f"✅ Оплата прошла успешно! Вам доступно +{total_generations} генераций.",
                chat_id=user_id,
                message_id=message_id
            )

        return web.json_response({"message": "Payment confirmed"}, status=200)

    except Exception as e:
        logging.error(f"Ошибка обработки вебхука: {e}")
        return web.json_response({"error": str(e)}, status=500)
    


async def handle_payment_reminder_webhook(request):
    """Обработчик вебхука для напоминания о неоплаченной генерации"""
    try:
        data = await request.json()
        user_id = data.get("user_id")

        if not user_id:
            return web.json_response({"error": "Missing user_id"}, status=400)

        # Отправляем сообщение пользователю
        message_text = (
            "⚠ Видим, что вы не оплатили пакет генерации.\n\n"
            "💡 Предлагаем вам попробовать один из наших пакетов:"
        )

        await bot.send_message(
            chat_id=user_id,
            text=message_text,
            reply_markup=get_packages_keyboard()
        )

        return web.json_response({"message": "Payment reminder sent"}, status=200)

    except Exception as e:
        logging.error(f"Ошибка обработки вебхука напоминания об оплате: {e}")
        return web.json_response({"error": str(e)}, status=500)


async def handle_avatar_ready_webhook(request):
    """Обработчик вебхука для уведомления о готовности аватара.
    
    При получении запроса отправляет пользователю сообщение:
    "Мы создали твой аватар, можем приступать к генерации фотографий"
    """
    try:
        data = await request.json()
        telegram_id = data.get("telegram_id")
        
        if not telegram_id:
            return web.json_response({"error": "Missing telegram_id"}, status=400)
        
        message_text = "Мы создали твой аватар, можем приступать к генерации фотографий"
        await bot.send_message(chat_id=telegram_id, text=message_text, reply_markup=main_menu_keyboard())
        
        return web.json_response({"message": "Уведомление отправлено"}, status=200)
    except Exception as e:
        logging.error(f"Ошибка обработки вебхука готовности аватара: {e}")
        return web.json_response({"error": str(e)}, status=500)


async def handle_generation_ready_webhook(request):
    """Обработчик вебхука для уведомления о готовности генерации.
    
    При получении запроса отправляет пользователю сгенерированные изображения.
    """
    try:
        data = await request.json()
        telegram_id = data.get("telegram_id")
        image_urls = data.get("image_urls")
        
        if not telegram_id or not image_urls:
            return web.json_response({"error": "Missing telegram_id или image_urls"}, status=400)
                
        # Формируем список медиа-объектов для отправки в виде галереи
        media = [InputMediaPhoto(media=url) for url in image_urls]
        
        # Отправляем медиа-группу с изображениями
        await bot.send_media_group(chat_id=telegram_id, media=media)
        
        # Отправляем сообщение о завершении генерации с клавиатурой главного меню
        await bot.send_message(chat_id=telegram_id, text="✅ Генерация завершена.", reply_markup=main_menu_keyboard())
        
        return web.json_response({"message": "Уведомление отправлено"}, status=200)
    except Exception as e:
        logging.error(f"Ошибка обработки вебхука генерации: {e}")
        return web.json_response({"error": str(e)}, status=500)

