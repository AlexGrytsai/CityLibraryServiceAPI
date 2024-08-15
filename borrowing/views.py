from typing import Type

from rest_framework import viewsets, mixins, serializers
from rest_framework.permissions import IsAdminUser
from rest_framework.serializers import Serializer

from borrowing.serializers import BorrowingSerializer


class BorrowingView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAdminUser,)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "create":
            return BorrowingSerializer

    def perform_create(self, serializer) -> None:
        book = serializer.validated_data["book"]

        if book.inventory == 0:
            raise serializers.ValidationError(
                {f"{book.title}": "The book is not available"}
            )

        book.inventory -= 1
        book.save()
