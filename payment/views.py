import stripe
from django.conf import settings
from django.http import JsonResponse, HttpRequest
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from payment.models import PaymentModel
from payment.serializers import PaymentListSerializer, PaymentDetailSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


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


class PaymentSuccessView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: HttpRequest) -> JsonResponse:
        session_id = request.GET.get("session_id")

        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == "paid":
            payment = PaymentModel.objects.get(session_id=session_id)
            payment.status = PaymentModel.Status.PAID
            payment.save()
            return JsonResponse({"message": "Payment successful!"})
        return JsonResponse({"message": "Payment not completed."}, status=400)


class PaymentCancelView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return JsonResponse(
            {"message": "Payment can be completed within 24 hours."}
        )
