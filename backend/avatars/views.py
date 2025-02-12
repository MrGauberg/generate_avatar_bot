from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Avatar
from .serializers import AvatarSerializer
from leonardo_service.services import LeonardoService
from django.conf import settings

class AvatarViewSet(viewsets.ModelViewSet):
    """Вьюсет для управления аватарами пользователей"""
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Фильтруем аватары по текущему пользователю"""
        return self.queryset.filter(user=self.request.user)


class AvatarUploadView(APIView):
    """Эндпоинт для загрузки 10 фото, создания датасета и обучения модели"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        user = request.user
        files = request.FILES.getlist("images")
        gender = request.data.get("gender", "male")
        
        if len(files) != settings.AVATAR_IMAGES_COUNT:
            return Response({"error": f"Должно быть ровно {settings.AVATAR_IMAGES_COUNT} изображений"}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем аватар и сохраняем изображения
        avatar_response = LeonardoService.create_avatar(user, gender, files)

        if "error" in avatar_response:
            return Response(avatar_response, status=status.HTTP_400_BAD_REQUEST)

        avatar_id = avatar_response["avatar_id"]

        # Создаем датасет
        print("Создаем датасет")
        # dataset_response = LeonardoService.create_dataset(avatar_id)
        dataset_response = {"dataset_id": 99, "status": "success"}

        if "error" in dataset_response:
            return Response(dataset_response, status=status.HTTP_400_BAD_REQUEST)

        # Загружаем изображения в датасет
        # upload_response = LeonardoService.upload_images_to_dataset(avatar_id)
        upload_response = {"status": "success"}

        if "error" in upload_response:
            return Response(upload_response, status=status.HTTP_400_BAD_REQUEST)

        # Запускаем обучение модели
        model_name = f"{user.username}_avatar_model"
        # train_response = LeonardoService.train_model(avatar_id, model_name)
        train_response = {"model_id": 77, "status": "training"}

        if "error" in train_response:
            return Response(train_response, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"avatar_id": avatar_id, "dataset_id": dataset_response["dataset_id"], "model_id": train_response["model_id"]},
            status=status.HTTP_201_CREATED
        )
