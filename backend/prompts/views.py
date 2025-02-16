# prompts/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import PromptCategory, PromptStyle
from .serializers import PromptCategorySerializer, PromptStyleSerializer

class PromptCategoryViewSet(viewsets.ModelViewSet):
    queryset = PromptCategory.objects.all()
    serializer_class = PromptCategorySerializer
    permission_classes = [IsAuthenticated]

class PromptStyleViewSet(viewsets.ModelViewSet):
    queryset = PromptStyle.objects.all()
    serializer_class = PromptStyleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.request.query_params.get('category')
        if category_id:
            return self.queryset.filter(category_id=category_id)
        else:
            return self.queryset.filter(category_id__isnull=True)
