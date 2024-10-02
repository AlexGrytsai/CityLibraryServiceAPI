from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APIClient

from payment.serializers import PaymentListSerializer, PaymentDetailSerializer
from payment.views import PaymentView


class TestPaymentView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )
        self.staff_user = get_user_model().objects.create_user(
            email="staff@example.com", password="staffpassword", is_staff=True
        )

    def test_payment_view_set(self):
        self.assertTrue(issubclass(PaymentView, viewsets.ReadOnlyModelViewSet))

    def test_payment_view_permission_classes(self):
        assert PaymentView.permission_classes == (IsAuthenticated,)

    def test_get_queryset_for_staff_user(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(reverse("payment:payment-list"))
        assert response.status_code == status.HTTP_200_OK

    def test_get_queryset_for_non_staff_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("payment:payment-list"))
        assert response.status_code == status.HTTP_200_OK

    def test_get_serializer_class_for_list_action(self):
        view = PaymentView()
        view.action = "list"
        assert view.get_serializer_class() == PaymentListSerializer

    def test_get_serializer_class_for_non_list_action(self):
        view = PaymentView()
        view.action = "retrieve"
        assert view.get_serializer_class() == PaymentDetailSerializer
