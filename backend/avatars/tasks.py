# avatars/tasks.py

from celery import shared_task
import requests
from django.conf import settings
from avatars.models import Avatar
from leonardo_service.services import LeonardoService

# URL для вебхука, на который будет отправлено уведомление при готовности элемента
WEBHOOK_URL = f"{settings.API_URL}/bot/element-ready/"

@shared_task
def check_element_ready_and_notify(avatar_id):
    """
    Проверяет статус обученного элемента.
    Если элемент готов (status == "COMPLETE"), отправляет вебхук с telegram_id.
    Если не готов, задача перепланируется на повторную проверку через 60 секунд.
    
    :param avatar_id: ID аватара, для которого проводится проверка
    :return: статус выполнения задачи
    """
    try:
        avatar = Avatar.objects.get(id=avatar_id)
    except Avatar.DoesNotExist:
        return {"error": f"Avatar с id {avatar_id} не найден", "status": "failed"}
    
    if not avatar.model_id:
        return {"error": "model_id отсутствует для данного аватара", "status": "failed"}
    
    # Проверяем статус элемента через API Leonardo
    status_result = LeonardoService.check_element_status(avatar.model_id)
    
    if status_result.get("status") == "COMPLETE":
        # Если элемент готов, отправляем вебхук с telegram_id пользователя
        telegram_id = avatar.user.telegram_id
        avatar.is_complete = True
        avatar.save()
        payload = {
            "telegram_id": telegram_id,
            "avatar_id": avatar_id,
            "model_id": avatar.model_id,
        }
        try:
            response = requests.post(WEBHOOK_URL, json=payload, timeout=5)
            response.raise_for_status()
            print(f"✅ Уведомление отправлено пользователю {telegram_id}")
            return {"status": "notified", "payload": payload}
        except requests.RequestException as e:
            error_msg = f"❌ Ошибка отправки вебхука для пользователя {telegram_id}: {e}"
            print(error_msg)
            return {"error": error_msg, "status": "failed"}
    else:
        # Если элемент еще не готов, перепланируем задачу на повтор через 60 секунд
        print(f"⏳ Статус элемента для avatar_id {avatar_id}: {status_result.get('status')}. Повтор через 60 секунд.")
        check_element_ready_and_notify.apply_async(args=[avatar_id], countdown=60)
        return {"status": "pending", "current_status": status_result.get("status")}
