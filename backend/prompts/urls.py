from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PromptCategoryViewSet, PromptStyleViewSet

router = DefaultRouter()
router.register(r'categories', PromptCategoryViewSet, basename='category')
router.register(r'styles', PromptStyleViewSet, basename='style')

urlpatterns = [
    path('', include(router.urls)),
]
