# packages/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum


from .serializers import PackageSerializer, PackageTypeSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Package, PackageType
from django.contrib.auth import get_user_model

User = get_user_model()


class PackageTypeViewSet(viewsets.ModelViewSet):
    queryset = PackageType.objects.all()
    serializer_class = PackageTypeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return super().get_queryset().order_by('amount')    

    


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticated]

    def get_user_packages(self, request, user_tg_id):
        """Возвращает список пакетов с доступными генерациями для пользователя"""
        user = get_object_or_404(User, telegram_id=user_tg_id)
        packages = self.get_queryset().filter(user=user, generations_remains__gt=0)
        serializer = self.get_serializer(packages, many=True)
        return Response(serializer.data)

    def get_total_generations(self, request, user_tg_id):
        """Возвращает общее количество доступных генераций у пользователя"""
        user = get_object_or_404(User, telegram_id=user_tg_id)

        total_generations = self.get_queryset().filter(user=user).aggregate(Sum("generations_remains"))["generations_remains__sum"] or 0

        return Response({"user_tg_id": user_tg_id, "total_generations": total_generations})




