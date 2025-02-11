# packages/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PackageViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'packages', PackageViewSet, basename='package')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
