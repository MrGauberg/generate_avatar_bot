# packages/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PackageTypeViewSet, PackageViewSet
from .views import PackageViewSet

router = DefaultRouter()
router.register(r'packages', PackageViewSet, basename='package')
router.register(r'package-types', PackageTypeViewSet, basename='package-type')

urlpatterns = [
    path('', include(router.urls)),
]
