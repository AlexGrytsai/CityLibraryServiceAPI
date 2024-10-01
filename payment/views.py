from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from payment.models import PaymentModel
from payment.serializers import PaymentSerializer


class PaymentView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentSerializer


    def get_queryset(self):
        if self.request.user.is_staff:
            return PaymentModel.objects.all()
        return PaymentModel.objects.filter(borrow__user=self.request.user)