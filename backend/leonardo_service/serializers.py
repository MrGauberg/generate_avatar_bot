# leonardo_service/serializers.py
from rest_framework import serializers
from .models import LeonardoGeneration

class LeonardoGenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeonardoGeneration
        fields = "__all__"
