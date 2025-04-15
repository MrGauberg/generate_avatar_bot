from django.urls import path, include
from .views import LeonardoGenerationViewSet


urlpatterns = [
    path('generate/', LeonardoGenerationViewSet.as_view({'post': 'generate'})),
]
