from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/packages/', include('packages.urls')),
    path('api/prompts/', include('prompts.urls')),
    path('api/avatars/', include('avatars.urls')),
    path('api/leonardo/', include('leonardo_service.urls')),
    path("api/payments/", include("payments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)