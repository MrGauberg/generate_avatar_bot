# packages/views.py
import requests
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.tele_bot import tele_bot

from .serializers import PackageSerializer, PackageTypeSerializer
import uuid
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from yookassa import Configuration, Payment
from .models import Package, PackageType
from django.contrib.auth import get_user_model

User = get_user_model()


class PackageTypeViewSet(viewsets.ModelViewSet):
    queryset = PackageType.objects.all()
    serializer_class = PackageTypeSerializer
    permission_classes = [IsAuthenticated]


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticated]

    def get_user_packages(self, request, user_tg_id):
        user = get_object_or_404(User, telegram_id=user_tg_id)
        
        avatars = self.get_queryset().filter(user=user).filter(generations_remains__gt=0)
        serializer = self.get_serializer(avatars, many=True)
        return Response(serializer.data)




