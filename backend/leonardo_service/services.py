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
        response = requests.post(url, headers=HEADERS, json={"name": f"dataset_{avatar_id}"})

        if not "error" in response.json():
            insert_datasets_one = response.json().get("insert_datasets_one")
            if insert_datasets_one:
                dataset_id = insert_datasets_one.get("id")
                if dataset_id:
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
    def train_element(avatar_id, element_name):
        """
        Обучает кастомный элемент на основе датасета и сохраняет её в аватар.
        :param avatar_id: ID аватара
        :param element_name: название кастомного элемента
        :return: model_id или ошибка
        """
        avatar = Avatar.objects.get(id=avatar_id)

        if not avatar.dataset_id:
            return {"error": "Dataset ID not found", "status": "failed"}

        url = f"{LEONARDO_BASE_URL}/models"
        payload = {
            "datasetId": avatar.dataset_id,
            "name": element_name,
            "instance_prompt":avatar.gender.gender,
            "resolution": 512,
            "focus": "Character",
            "status": "COMPLETE",
            "baseModel": "SDXL_1_0",
            "learningRate": 0.000001,
            "trainingEpoch": 100,
            "instancePrompt": "a photorealistic image of elena_face_1",
            "trainTextEncoder": True
        }

        response = requests.post(url, json=payload, headers=HEADERS)

        if not "error" in response.json():
            taraining_job = response.json().get("sdTrainingJob")
            if taraining_job:
                element_id = taraining_job.get("userLoraId")
                if element_id:
                    api_credit_cost = taraining_job.get("apiCreditCost")
                    avatar.model_id = element_id
                    avatar.api_credit_cost = api_credit_cost
                    avatar.save()
                    return {"model_id": element_id, "status": "training", "api_credit_cost": api_credit_cost}

        return {"error": response.json(), "status": "failed"}
    

    @staticmethod
    def check_element_status(element_id):
        """
        Проверяет готовность натренированного элемента по его ID.
        Возвращает статус элемента и все полученные данные.
        
        :param element_id: ID элемента для проверки
        :return: словарь с результатами проверки или информацией об ошибке
        """
        url = f"{LEONARDO_BASE_URL}/elements/{element_id}"
        response = requests.get(url, headers=HEADERS)
        
        try:
            data = response.json()
        except json.JSONDecodeError:
            return {"error": "Невозможно декодировать ответ", "status": "failed"}
        
        if response.status_code == 200:
            element_status = data.get("status")
            if element_status == "COMPLETE":
                Avatar.objects.filter(model_id=element_id).update(is_complete=True, element_name=data.get("name"))
                return {"element_id": element_id, "status": "COMPLETE", "details": data}
            else:
                return {"element_id": element_id, "status": element_status, "details": data}
        else:
            return {"error": data, "status": "failed"}


    @staticmethod
    def generate_image(user, prompt):
        """Создаёт изображение с использованием обученной модели"""
        url = f"{LEONARDO_BASE_URL}/generations"

        model_id = "5c232a9e-9061-4777-980a-ddc8e65647c6"
        width=1024
        height=1024
        guidance_scale=7
        payload = {
            "alchemy": True,
            "height": height,
            "modelId": model_id,
            "num_images": 1,
            "presetStyle": "NONE",
            "prompt": f"elena_face_1 {prompt}",
            "width": width,
            "sd_version": "SDXL_LIGHTNING",
            "userElements": [
                {
                "userLoraId": 35744,
                "weight": 1
                }
            ],
            "expandedDomain": True,
            "highResolution": True,
            "num_inference_steps": 25,
            "photoReal": False,
            "promptMagic": False,
            "guidance_scale": 7,
            "enhancePrompt": False
            }

        response = requests.post(url, json=payload, headers=HEADERS)

        if not "error" in response.json():
            sd_generation_job = response.json().get("sdGenerationJob")
            if sd_generation_job:
                generation_id = sd_generation_job.get("generationId")
                if generation_id:
                    api_credit_cost = sd_generation_job.get("apiCreditCost")
                    LeonardoGeneration.objects.create(
                        user=user,
                        model_id=model_id,
                        prompt=prompt,
                        width=width,
                        height=height,
                        guidance_scale=guidance_scale,
                        generation_id=generation_id,
                        status="pending",
                        api_credit_cost=api_credit_cost,
                    )
                    return {"generation_id": generation_id, "status": "pending", "api_credit_cost": api_credit_cost}

        return {"error": response.json(), "status": "failed"}
    
    @staticmethod
    def get_generation_details(generation_id):
        """
        Получает данные генерации по её ID.
        
        :param generation_id: ID генерации
        :return: словарь с данными генерации или ошибкой
        """
        url = f"{LEONARDO_BASE_URL}/generations/{generation_id}"
        response = requests.get(url, headers=HEADERS)
        try:
            data = response.json()
        except json.JSONDecodeError:
            return {"error": "Невозможно декодировать ответ", "status": "failed"}
        
        if response.status_code == 200:
            return data
        else:
            return {"error": data, "status": "failed"}

