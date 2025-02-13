# packages/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PackageTypeViewSet, PackageViewSet
from .views import CreatePaymentView, PaymentWebhookView, PackageViewSet

router = DefaultRouter()
router.register(r'packages', PackageViewSet, basename='package')
router.register(r'package-types', PackageTypeViewSet, basename='package-type')

urlpatterns = [
    path('', include(router.urls)),
    path("yookassa-payment/create/", CreatePaymentView.as_view(), name="create_payment"),
    path("yookassa/webhook/", PaymentWebhookView.as_view(), name="payment_webhook"),
]
