# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'telegram_id')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    photo_format = serializers.CharField(source='settings.photo_format')
    avatars_amount_available = serializers.IntegerField(source='settings.avatars_amount_available')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'telegram_id', 'photo_format', 'avatars_amount_available', 'is_authorized', 'is_active')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            telegram_id=validated_data.get('telegram_id', None)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
