# packages/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import PackageSerializer, PackageTypeSerializer
import uuid
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from yookassa import Configuration, Payment
from .models import Package, PackageType, Payment as PaymentModel
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

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


# Настраиваем API ЮKassa
Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


class CreatePaymentView(APIView):
    """Создание платежа через ЮKassa"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        email = request.data.get("email")
        package_type_id = request.data.get("package_type_id")

        package_type = get_object_or_404(PackageType, id=package_type_id)
        amount = package_type.amount

        payment_id = str(uuid.uuid4())

        try:
            user = User.objects.create(telegram_id=telegram_id, email=email, username=email)
            package = Package.objects.create(
                    user=user,
                    package_type=package_type,
                    generations_remains=package_type.total_generations
                )

            payment_data = {
                "amount": {"value": str(amount), "currency": "RUB"},
                "confirmation": {"type": "redirect", "return_url": "https://your-site.com/success"},
                "capture": True,
                "description": f"Покупка генераций {package_type.name}",
                "metadata": {"payment_id": payment_id, "package_id": package.id, "user_id": user.id}
            }

            payment = Payment.create(payment_data)
            PaymentModel.objects.create(
                user=user,
                package=package,
                payment_id=payment_id,
                amount=amount,
                status="pending"
            )

            return Response({"payment_url": payment.confirmation.confirmation_url}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentWebhookView(APIView):
    """Вебхук ЮKassa для обновления статуса платежа"""

    def post(self, request):
        event_data = request.data
        metadata = event_data.get("object", {}).get("metadata", {})
        payment_id = metadata.get("payment_id")
        package_id = metadata.get("package_id")
        status_update = event_data.get("object", {}).get("status")

        user_id = metadata.get("user_id", None)

        if not payment_id or not status_update or not package_id or not user_id:
            return Response({"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = PaymentModel.objects.get(payment_id=payment_id)
            payment.status = status_update
            payment.save()

            if status_update == "succeeded":
                user = get_object_or_404(User, id=user_id)
                package = get_object_or_404(Package, id=package_id)
                package.is_active = True
                user.is_authorized = True
                user.save()
                package.save()

            return Response({"message": "Payment status updated"}, status=status.HTTP_200_OK)

        except PaymentModel.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)


