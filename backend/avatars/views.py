import uuid
import requests
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Avatar, AvatarGender, AvatarSettings
from .serializers import AvatarAvatarGenderSerializer, AvatarSerializer
from leonardo_service.services import LeonardoService
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from yookassa import Configuration, Payment


User = get_user_model()

class AvatarViewSet(viewsets.ModelViewSet):
    """Вьюсет для управления аватарами пользователей"""
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAuthenticated]

    def get_user_avatars(self, request, user_tg_id):
        user = get_object_or_404(User, telegram_id=user_tg_id)
        
        avatars = self.get_queryset().filter(user=user)
        serializer = self.get_serializer(avatars, many=True)
        return Response(serializer.data)
    
    def is_active(self, request, *args, **kwargs):
        avatar = self.get_object()
        avatar.is_active = True
        avatar.save()
        Avatar.objects.exclude(id=avatar.id).update(is_active=False)
        return JsonResponse({"detail": "Аватар успешно активирован"})
    



class AvatarUploadView(APIView):
    """Эндпоинт для загрузки 10 фото, создания датасета и обучения модели"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        tg_user_id = request.data.get("tg_user_id")  
        files = request.FILES.getlist("images")
        gender = request.data.get("gender")
        
        if len(files) != settings.IMAGES_COUNT:
            return Response({"error": f"Должно быть ровно {settings.IMAGES_COUNT} изображений"}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем аватар и сохраняем изображения
        user = get_object_or_404(User, telegram_id=tg_user_id)
        avatar_response = LeonardoService.create_avatar(user, gender, files)

        if "error" in avatar_response:
            return Response(avatar_response, status=status.HTTP_400_BAD_REQUEST)

        avatar_id = avatar_response["avatar_id"]

        # Создаем датасет
        print("Создаем датасет")
        dataset_response = LeonardoService.create_dataset(avatar_id)
        # dataset_response = {"dataset_id": 99, "status": "success"}

        if "error" in dataset_response:
            return Response(dataset_response, status=status.HTTP_400_BAD_REQUEST)

        # Загружаем изображения в датасет
        upload_response = LeonardoService.upload_images_to_dataset(avatar_id)
        # upload_response = {"status": "success"}

        if "error" in upload_response:
            return Response(upload_response, status=status.HTTP_400_BAD_REQUEST)

        # Запускаем обучение модели
        model_name = f"{user.username}_avatar_model"
        train_response = LeonardoService.train_model(avatar_id, model_name)
        # train_response = {"model_id": 77, "status": "training"}

        if "error" in train_response:
            return Response(train_response, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"avatar_id": avatar_id, "dataset_id": dataset_response["dataset_id"], "model_id": train_response["model_id"]},
            status=status.HTTP_201_CREATED
        )


class CheckAvatarSlotsView(APIView):
    """Проверяет количество доступных слотов у пользователя"""
    permission_classes = [IsAuthenticated]

    def get(self, request, user_tg_id):
        user = get_object_or_404(User, telegram_id=user_tg_id)
        total_avatars = user.avatars.count()
        available_slots = user.settings.avatars_amount_available > total_avatars
        return Response({"can_add_avatar": available_slots})

class AvatarGenderView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AvatarGender.objects.all()
    serializer_class = AvatarAvatarGenderSerializer


def get_avatar_price(request):
    """Возвращает стоимость добавления аватара"""
    settings = AvatarSettings.objects.first()
    return JsonResponse({"price": settings.price if settings else 490.00})