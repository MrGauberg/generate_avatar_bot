from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvatarViewSet, AvatarUploadView

router = DefaultRouter()
router.register(r'avatars', AvatarViewSet, basename='avatar')

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', AvatarUploadView.as_view(), name='avatar-upload'),
]
