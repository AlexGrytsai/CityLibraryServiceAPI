import stripe
from django.conf import settings
from django.http import JsonResponse, HttpRequest
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from notification.tasks import notify_successfully_payed
from payment.models import PaymentModel
from payment.serializers import PaymentListSerializer, PaymentDetailSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


@extend_schema_view(
    list=extend_schema(
        responses={
            200: PaymentListSerializer,
        },
        description="Retrieve list of payments for the current user "
        "or all payments for staff.",
    ),
    retrieve=extend_schema(
        responses={
            200: PaymentDetailSerializer,
        },
        description="Retrieve detailed information about a specific payment.",
    ),
)
class PaymentView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return PaymentModel.objects.all()
        return PaymentModel.objects.filter(borrow__user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        return PaymentDetailSerializer


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="session_id",
                description="Stripe session ID to verify the payment",
                required=True,
                type=str,
            ),
        ],
        responses={
            200: OpenApiResponse(description="Payment successful!"),
            400: OpenApiResponse(description="Payment not completed."),
        },
        description="Verify Stripe payment by session_id "
        "and update payment status.",
    )
)
class PaymentSuccessView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: HttpRequest) -> JsonResponse:
        session_id = request.GET.get("session_id")

        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == "paid":
            payment = PaymentModel.objects.get(session_id=session_id)
            payment.status = PaymentModel.Status.PAID
            payment.save()

            message = (
                f"Payment successful for {payment.borrow.user.email} "
                f"(id={payment.borrow.user.id}) \n"
                f"for borrowing ID {payment.borrow.id}."
            )

            notify_successfully_payed.delay(message)
            return JsonResponse({"message": "Payment successful!"})
        return JsonResponse({"message": "Payment not completed."}, status=400)


@extend_schema_view(
    get=extend_schema(
        responses={
            200: OpenApiResponse(
                description="Payment can be completed within 24 hours."
            )
        },
        description="Notify user that payment can be completed within 24 hours.",
    )
)
class PaymentCancelView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return JsonResponse(
            {"message": "Payment can be completed within 24 hours."}
        )
