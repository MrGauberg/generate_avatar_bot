import requests
from django.conf import settings


class TeleBot:

    def send_message(self, chat_id, text):
        bot_token = settings.BOT_TOKEN
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data)
        return response.json()


tele_bot = TeleBot()
