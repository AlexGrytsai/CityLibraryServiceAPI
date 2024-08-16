from typing import Type

from rest_framework import viewsets, mixins, serializers
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.serializers import Serializer

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingListSerializer, BorrowingDetailSerializer


class BorrowingView(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Borrowing.objects.all().select_related("user", "book")

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_staff:
            return super(BorrowingView, self).get_queryset()
        return super().get_queryset().filter(user=current_user)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "create":
            return BorrowingSerializer
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        return BorrowingSerializer

    def perform_create(self, serializer) -> None:
        book = serializer.validated_data["book"]

        if book.inventory == 0:
            raise serializers.ValidationError(
                {f"{book.title}": "The book is not available"}
            )

        book.inventory -= 1
        book.save()

        serializer.save(user=self.request.user)
