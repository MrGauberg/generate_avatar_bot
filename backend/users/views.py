# users/views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

User = get_user_model()

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Кастомный класс для входа, если надо расширить логику
    """
    pass

User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, telegram_id):
        instance = get_object_or_404(User, telegram_id=telegram_id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def set_photo_format(self, request, telegram_id):
        user = get_object_or_404(User, telegram_id=telegram_id)
        user.settings.photo_format = request.data.get('photo_format')
        user.settings.save()
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

        
