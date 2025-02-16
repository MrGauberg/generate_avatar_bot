# bot/handlers/webhooks.py

from aiohttp import web
from aiogram import Bot
from bot.config import Settings
import logging

from bot.services.redis_client import redis_client

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
                f"✅ Оплата прошла успешно! Вам доступно {total_generations} генераций.",
                chat_id=user_id,
                message_id=message_id
            )

        return web.json_response({"message": "Payment confirmed"}, status=200)

    except Exception as e:
        logging.error(f"Ошибка обработки вебхука: {e}")
        return web.json_response({"error": str(e)}, status=500)
