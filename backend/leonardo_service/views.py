# leonardo_service/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import LeonardoGeneration
from .serializers import LeonardoGenerationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from .services import LeonardoService
from leonardo_service.tasks import check_generation_ready_and_notify
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


class LeonardoGenerationViewSet(viewsets.ModelViewSet):
    """API для управления генерациями"""
    queryset = LeonardoGeneration.objects.all()
    serializer_class = LeonardoGenerationSerializer
    permission_classes = [IsAuthenticated]

    def generate(self, request):
        """
        Эндпоинт для генерации изображений.
        Ожидает параметр prompt в теле запроса.
        При успешной генерации запускается celery-задача для периодической проверки статуса генерации.
        """
        prompt = request.data.get("prompt")
        telegram_id = request.data.get("telegram_id")
        if not prompt:
            return Response({"error": "Параметр 'prompt' обязателен."}, status=400)
        
        user = get_object_or_404(User, telegram_id=telegram_id)

        # Вызов генерации изображения через LeonardoService
        result = LeonardoService.generate_image(user, prompt)
        print(result)
        if "error" in result:
            return Response(result, status=400)
        
        generation_id = result.get("generation_id")
        # Импорт celery-задачи и её запуск для проверки статуса генерации каждую секунду
        check_generation_ready_and_notify.delay(generation_id)
        
        return Response(result, status=201)

