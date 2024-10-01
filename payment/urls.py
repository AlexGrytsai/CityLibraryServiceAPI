from django.urls import path, include
from rest_framework import routers

from payment.views import PaymentView, payment_success, payment_cancel

router = routers.DefaultRouter()

router.register("payments", PaymentView, basename="payment")

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("success/", payment_success, name="payment-success"),
    path("cancel/", payment_cancel, name="payment-cancel"),
]

app_name = "payment"
