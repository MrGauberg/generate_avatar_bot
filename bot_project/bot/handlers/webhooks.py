# bot/handlers/webhooks.py

from aiohttp import web
from aiogram import Bot
from bot.config import Settings
import logging

bot = Bot(token=Settings.bot.TOKEN)

IMAGES_COUNT = Settings.service.IMAGES_COUNT

async def handle_payment_webhook(request):
    """Обработчик вебхука для подтверждения платежа"""
    try:
        data = await request.json()
        user_id = data.get("user_id")
        message_id = data.get("message_id")

        if not user_id or not message_id:
            return web.json_response({"error": "Missing user_id or message_id"}, status=400)

        await bot.edit_message_text(
            f"✅ Оплата прошла успешно!\nТеперь отправьте {IMAGES_COUNT} фото для создания аватара.",
            chat_id=user_id,
            message_id=message_id
        )

        return web.json_response({"message": "Payment confirmed"}, status=200)

    except Exception as e:
        logging.error(f"Ошибка обработки вебхука: {e}")
        return web.json_response({"error": str(e)}, status=500)



async def start_webhook_server():
    """Запускаем веб-сервер для обработки вебхуков"""
    link = "/payment-webhook/"
    port = 8090 
    ip = "0.0.0.0"
    app = web.Application()
    app.router.add_post(link, handle_payment_webhook)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, ip, port)
    await site.start()
    logging.info(f"Webhook server запущен на http://{ip}:{port}{link}")
