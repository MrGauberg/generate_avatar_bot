from rest_framework import serializers
from .models import Avatar, AvatarGender, AvatarImage
from django.conf import settings


class AvatarImageSerializer(serializers.ModelSerializer):
    """Сериализатор для изображений аватара"""

    class Meta:
        model = AvatarImage
        fields = ["id", "image"]

class AvatarAvatarGenderSerializer(serializers.ModelSerializer):
    """Сериализатор для изображений аватара"""

    class Meta:
        model = AvatarGender
        fields = ["id", "gender"]


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор для аватара"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    images = AvatarImageSerializer(many=True, read_only=True)

    class Meta:
        model = Avatar
        fields = [
            "id",
            "user",
            "dataset_id",
            "model_id",
            "gender",
            "created_at",
            "images",
            "name",
            "is_active",
        ]


class AvatarUploadSerializer(serializers.Serializer):
    f"""Сериализатор для загрузки {settings.IMAGES_COUNT} изображений"""

    images = serializers.ListField(
        child=serializers.ImageField(),
        min_length=settings.IMAGES_COUNT,
        max_length=settings.IMAGES_COUNT,
        error_messages={
            "min_length": f"Должно быть ровно {settings.IMAGES_COUNT} изображений",
            "max_length": f"Должно быть ровно {settings.IMAGES_COUNT} изображений",
        },
    )
    gender = serializers.ChoiceField(
        choices=["male", "female", "child"], default="male"
    )
