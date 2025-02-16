import requests
import json
from django.conf import settings
from django.core.files.storage import default_storage

from avatars.models import Avatar, AvatarGender, AvatarImage
from .models import LeonardoGeneration



LEONARDO_API_KEY = settings.LEONARDO_API_KEY
LEONARDO_BASE_URL = "https://cloud.leonardo.ai/api/rest/v1"

HEADERS = {
    "Authorization": f"Bearer {LEONARDO_API_KEY}",
    "Content-Type": "application/json",
}


class LeonardoService:
    """Класс-сервис для взаимодействия с API Leonardo.AI"""

    @staticmethod
    def create_avatar(user, gender, image_files):
        """
        Создаёт пустой аватар и сохраняет загруженные файлы изображений.
        :param user: объект пользователя
        :param gender: пол (male, female, child)
        :param image_files: список файлов изображений
        :return: ID аватара
        """
        gender = AvatarGender.objects.get(id=gender)
        avatar = Avatar.objects.create(user=user, gender=gender, is_active=True)
        Avatar.objects.exclude(id=avatar.id).update(is_active=False)

        for image_file in image_files:
            image_path = default_storage.save(f"avatars/{image_file.name}", image_file)
            AvatarImage.objects.create(avatar=avatar, image=image_path)

        return {"avatar_id": avatar.id, "status": "created"}

    @staticmethod
    def create_dataset(avatar_id):
        """
        Создаёт пустой датасет и привязывает его к аватару.
        :param avatar_id: ID аватара
        :return: dataset_id или ошибка
        """
        url = f"{LEONARDO_BASE_URL}/datasets"
        response = requests.post(url, headers=HEADERS)

        if response.status_code == 201:
            dataset_id = response.json().get("datasetId")
            avatar = Avatar.objects.get(id=avatar_id)
            avatar.dataset_id = dataset_id
            avatar.save()
            return {"dataset_id": dataset_id, "status": "success"}

        return {"error": response.json(), "status": "failed"}

    @staticmethod
    def get_presigned_url(dataset_id, extension="jpg"):
        """
        Получает предварительно подписанный URL для загрузки изображения.
        :param dataset_id: ID датасета
        :param extension: формат изображения (jpg, png и т.д.)
        :return: URL для загрузки или ошибка
        """
        url = f"{LEONARDO_BASE_URL}/datasets/{dataset_id}/upload"
        payload = {"extension": extension}
        response = requests.post(url, json=payload, headers=HEADERS)

        if response.status_code == 200:
            return response.json()["uploadDatasetImage"]

        return {"error": response.json(), "status": "failed"}

    @staticmethod
    def upload_images_to_dataset(avatar_id):
        """
        Загружает изображения, связанные с аватаром, в датасет Leonardo.AI.
        :param avatar_id: ID аватара
        :return: статус загрузки
        """
        avatar = Avatar.objects.get(id=avatar_id)

        if not avatar.dataset_id:
            return {"error": "Dataset ID not found", "status": "failed"}

        for image_obj in avatar.images.all():
            presigned_data = LeonardoService.get_presigned_url(avatar.dataset_id)

            if "error" in presigned_data:
                return presigned_data  # Возвращаем ошибку

            url = presigned_data["url"]
            fields = json.loads(presigned_data["fields"])

            with default_storage.open(image_obj.image.name, "rb") as image_file:
                files = {"file": (fields["key"], image_file)}
                response = requests.post(url, data=fields, files=files)

            if response.status_code != 204:
                return {"error": response.content, "status": "failed"}

        return {"status": "uploaded"}

    @staticmethod
    def train_model(avatar_id, model_name):
        """
        Обучает кастомную модель на основе датасета и сохраняет её в аватар.
        :param avatar_id: ID аватара
        :param model_name: название кастомной модели
        :return: model_id или ошибка
        """
        avatar = Avatar.objects.get(id=avatar_id)

        if not avatar.dataset_id:
            return {"error": "Dataset ID not found", "status": "failed"}

        url = f"{LEONARDO_BASE_URL}/models/train"
        payload = {"datasetId": avatar.dataset_id, "name": model_name}

        response = requests.post(url, json=payload, headers=HEADERS)

        if response.status_code == 202:
            model_id = response.json().get("modelId")
            avatar.model_id = model_id
            avatar.save()
            return {"model_id": model_id, "status": "training"}

        return {"error": response.json(), "status": "failed"}

    @staticmethod
    def generate_image(user, model_id, prompt, width=512, height=512, guidance=7.5):
        """Создаёт изображение с использованием обученной модели"""
        url = f"{LEONARDO_BASE_URL}/generations"
        payload = {
            "modelId": model_id,
            "prompt": prompt,
            "width": width,
            "height": height,
            "guidanceScale": guidance,
        }

        response = requests.post(url, json=payload, headers=HEADERS)

        if response.status_code == 201:
            data = response.json()
            LeonardoGeneration.objects.create(
                user=user,
                model_id=model_id,
                prompt=prompt,
                width=width,
                height=height,
                guidance=guidance,
                generation_id=data["generationId"],
                status="pending",
            )
            return {"generation_id": data["generationId"], "status": "started"}

        return {"error": response.json(), "status": "failed"}
