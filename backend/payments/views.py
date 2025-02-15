import uuid
import requests
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from yookassa import Payment, Configuration
from django.conf import settings
from avatars.models import AvatarSettings
from packages.models import Package, PackageType
from payments.models import PaymentRecord
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


# Настраиваем API ЮKassa
Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


class BasePaymentView(APIView):
    """Базовый класс для создания платежей"""

    permission_classes = [IsAuthenticated]

    def create_payment(self, user, amount, description, metadata):
        payment_id = str(uuid.uuid4())

        payment_data = {
            "amount": {"value": str(amount), "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": f"https://t.me/{settings.BOT_TG}",
            },
            "capture": True,
            "description": description,
            "metadata": {**metadata, "payment_id": payment_id},
        }

        payment = Payment.create(payment_data)

        # Сохраняем платеж в БД
        PaymentRecord.objects.create(
            user=user,
            payment_id=payment_id,
            amount=amount,
            status="pending",
            metadata=metadata,
        )

        return payment.confirmation.confirmation_url


class CreatePackagePaymentView(BasePaymentView):
    """Создание платежа за пакеты генераций"""

    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        package_type_id = request.data.get("package_type_id")
        message_id = request.data.get("message_id")
        email = request.data.get("email")

        print(request.data)

        user, created = User.objects.get_or_create(
            telegram_id=telegram_id, defaults={"email": email, "username": email}
        )
        package = get_object_or_404(PackageType, id=package_type_id)

        Package.objects.create(
            user=user,
            package_type=package,
            generations_remains=package.total_generations,
        )

        payment_url = self.create_payment(
            user,
            package.amount,
            f"Покупка генераций {package.name}",
            {
                "telegram_id": telegram_id,
                "message_id": message_id,
                "type": "package",
                "package_id": package.id,
            },
        )

        return Response({"payment_url": payment_url}, status=201)


class CreateAvatarPaymentView(BasePaymentView):
    """Создание платежа за дополнительный слот аватара"""

    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        message_id = request.data.get("message_id")

        user = get_object_or_404(User, telegram_id=telegram_id)
        avatar_price = AvatarSettings.objects.first().price

        payment_url = self.create_payment(
            user,
            avatar_price,
            "Покупка слота для аватара",
            {"telegram_id": telegram_id, "message_id": message_id, "type": "avatar"},
        )

        return Response({"payment_url": payment_url}, status=201)


class YooKassaWebhookView(APIView):
    """Общий вебхук для обработки платежей ЮKassa"""

    def post(self, request):
        event_data = request.data
        metadata = event_data.get("object", {}).get("metadata", {})
        payment_id = metadata.get("payment_id")
        telegram_id = metadata.get("telegram_id")
        message_id = metadata.get("message_id")
        payment_type = metadata.get("type")
        status_update = event_data.get("object", {}).get("status")

        if not payment_id or not status_update or not telegram_id or not message_id:
            return Response(
                {"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payment = PaymentRecord.objects.get(payment_id=payment_id)
            payment.status = status_update
            payment.save()

            if status_update == "succeeded":
                user = get_object_or_404(User, telegram_id=telegram_id)

                if payment_type == "package":
                    package_id = metadata.get("package_id")
                    package = get_object_or_404(Package, id=package_id)
                    package.is_active = True
                    user.is_authorized = True
                    package.save()
                elif payment_type == "avatar":
                    user.avatars_amount_available += 1
                user.save()

                # Уведомляем бота о статусе оплаты
                webhook_url = f"{settings.API_URL}/bot/payment-webhook/"
                requests.post(
                    webhook_url, json={"user_id": telegram_id, "message_id": message_id}
                )

            return Response(
                {"message": "Payment status updated"}, status=status.HTTP_200_OK
            )

        except PaymentRecord.DoesNotExist:
            return Response(
                {"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
            )
