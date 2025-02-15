from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvatarViewSet, AvatarUploadView, get_avatar_price

router = DefaultRouter()
router.register(r'avatars', AvatarViewSet, basename='avatar')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/activate/', AvatarViewSet.as_view({'patch': 'is_active'}), name='avatar-activate'),
    path('<int:user_tg_id>/', AvatarViewSet.as_view({'get': 'get_user_avatars'}), name='avatar-activate'),
    path('upload/', AvatarUploadView.as_view(), name='avatar-upload'),
    path("avatar/price/", get_avatar_price, name="get_avatar_price"),
    path("check-slots/<int:user_tg_id>/", get_avatar_price, name="check-avatar-slots"),
]
