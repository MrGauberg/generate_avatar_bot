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
    path('user-packages/<int:user_tg_id>/', PackageViewSet.as_view({'get': 'get_user_packages'}), name='user-packages'),
    path('total-generations/<int:user_tg_id>/', PackageViewSet.as_view({'get': 'get_total_generations'}), name='total-generations'),
]
