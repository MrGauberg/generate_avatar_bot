# leonardo_service/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import LeonardoGeneration
from .serializers import LeonardoGenerationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class LeonardoGenerationViewSet(viewsets.ModelViewSet):
    """ API для управления генерациями """
    queryset = LeonardoGeneration.objects.all()
    serializer_class = LeonardoGenerationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """ Получить статус генерации """
        generation = self.get_object()
        status = get_generation_status(generation.generation_id)
        return Response(status)

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """ Получить изображения после генерации """
        generation = self.get_object()
        images = get_generated_images(generation.generation_id)
        return Response(images)
