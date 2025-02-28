# payments/tasks.py

from celery import shared_task
from django.utils.timezone import now, timedelta
import requests
from django.conf import settings
from payments.models import PaymentRecord

BOT_WEBHOOK_URL = f"{settings.API_URL}/bot/payment-reminder/"

@shared_task
def check_unpaid_payments():
    """
    Проверяет неоплаченные платежи (`pending` и `canceled`), созданные более X минут назад, 
    отправляет вебхук в бота и удаляет их после напоминания.
    """
    expired_time = now() - timedelta(minutes=settings.PAYMENT_REMINDER_DELAY)

    unpaid_payments = PaymentRecord.objects.filter(
        status__in=["pending", "canceled"], created_at__lte=expired_time
    )

    notified_users = []
    errors = []

    for payment in unpaid_payments:
        user_tg_id = getattr(payment.user, "telegram_id", None)
        
        if not user_tg_id:
            continue

        payload = {"user_id": user_tg_id}
        
        try:
            response = requests.post(BOT_WEBHOOK_URL, json=payload, timeout=5)
            response.raise_for_status()
            notified_users.append(user_tg_id)
            print(f"✅ Напоминание отправлено пользователю {user_tg_id}")

            payment.delete()

        except requests.RequestException as e:
            error_msg = f"❌ Ошибка отправки вебхука пользователю {user_tg_id}: {e}"
            errors.append(error_msg)
            print(error_msg)

    return {
        "processed_payments": len(unpaid_payments),
        "notified_users": notified_users,
        "errors": errors
    }
