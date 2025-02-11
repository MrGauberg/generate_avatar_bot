# prompts/serializers.py
from rest_framework import serializers
from .models import PromptCategory, PromptStyle

class PromptCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptCategory
        fields = '__all__'

class PromptStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptStyle
        fields = '__all__'
