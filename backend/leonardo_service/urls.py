# leonardo_service/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeonardoGenerationViewSet

router = DefaultRouter()
router.register(r'generations', LeonardoGenerationViewSet, basename='leonardo-generation')

urlpatterns = [
    path('', include(router.urls)),
]
