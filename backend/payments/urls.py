from django.urls import path
from .views import CreatePackagePaymentView, CreateAvatarPaymentView, YooKassaWebhookView

urlpatterns = [
    path("package/", CreatePackagePaymentView.as_view(), name="create-package-payment"),
    path("avatar/", CreateAvatarPaymentView.as_view(), name="create-avatar-payment"),
    path("yookassa-webhook/", YooKassaWebhookView.as_view(), name="yookassa-webhook"),
]
