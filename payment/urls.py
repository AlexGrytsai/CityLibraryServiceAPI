from django.urls import path, include
from rest_framework import routers

from payment.views import PaymentView, PaymentCancelView, PaymentSuccessView

router = routers.DefaultRouter()

router.register("payments", PaymentView, basename="payment")

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("success/", PaymentSuccessView.as_view(), name="payment-success"),
    path("cancel/", PaymentCancelView.as_view(), name="payment-cancel"),
]

app_name = "payment"
