from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserViewSet


urlpatterns = [
    path('<int:telegram_id>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('set_photo_format/<int:telegram_id>/', UserViewSet.as_view({'post': 'set_photo_format'})),
    path('set_god_mode/<int:telegram_id>/', UserViewSet.as_view({'post': 'set_god_mode'})),
    path('register/', RegisterView.as_view(), name='user-register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

