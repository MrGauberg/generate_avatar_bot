# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Получение access и refresh токена
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление access-токена
]

