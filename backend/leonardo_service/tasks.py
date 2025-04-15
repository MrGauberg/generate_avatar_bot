from celery import shared_task
import requests
from django.conf import settings
from avatars.models import Avatar
from .models import LeonardoGeneration
from .services import LeonardoService

# URL вебхука для уведомления бота о готовности генерации
WEBHOOK_GENERATION_READY_URL = f"{settings.API_URL}/bot/generation-ready/"

@shared_task
def check_generation_ready_and_notify(generation_id):
    """
    Проверяет статус генерации по ее ID.
    Если статус равен "COMPLETE", извлекает ссылки на изображения и отправляет вебхук боту.
    Если статус не "COMPLETE", задача перепланируется через 1 секунду.
    
    :param generation_id: ID генерации (поле generation_id модели LeonardoGeneration)
    :return: результат выполнения задачи
    """
    try:
        generation_obj = LeonardoGeneration.objects.get(generation_id=generation_id)
    except LeonardoGeneration.DoesNotExist:
        return {"error": f"LeonardoGeneration с id {generation_id} не найден", "status": "failed"}

    details = LeonardoService.get_generation_details(generation_id)
    
    # Проверяем статус генерации внутри вложенного поля "generations_by_pk"
    generation_data = details.get("generations_by_pk", {})
    current_status = generation_data.get("status")
    
    if current_status == "COMPLETE":
        # Извлекаем ссылки на изображения
        images = generation_data.get("generated_images", [])
        image_urls = [img.get("url") for img in images if img.get("url")]
        
        # Готовим payload для вебхука
        telegram_id = generation_obj.user.telegram_id
        payload = {
            "telegram_id": telegram_id,
            "generation_id": generation_id,
            "image_urls": image_urls,
        }
        
        try:
            response = requests.post(WEBHOOK_GENERATION_READY_URL, json=payload, timeout=5)
            response.raise_for_status()
            print(f"✅ Уведомление отправлено пользователю {telegram_id}")
            generation_obj.status = "notified"
            generation_obj.save()
            return {"status": "notified", "payload": payload}
        except requests.RequestException as e:
            error_msg = f"❌ Ошибка отправки вебхука для пользователя {telegram_id}: {e}"
            print(error_msg)
            return {"error": error_msg, "status": "failed"}
    else:
        print(f"⏳ Генерация {generation_id} не готова (текущий статус: {current_status}). Повтор через 1 секунду.")
        check_generation_ready_and_notify.apply_async(args=[generation_id], countdown=1)
        return {"status": "pending", "current_status": current_status}
