import logging
from typing import Type

from rest_framework import viewsets, mixins, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)

logger = logging.getLogger("my_debug")


class BorrowingView(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Borrowing.objects.all().select_related("user", "book")

    def get_queryset(self):
        current_user = self.request.user

        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if user_id and current_user.is_staff:
            logger.info(
                f"{current_user} used 'user_id'={user_id} "
                f"for filter borrowed books"
            )
            return super().get_queryset().filter(user__id=user_id)
        if is_active:
            logger.info(
                f"{current_user} used 'is_active'={is_active} "
                f"for filter borrowed books"
            )
            if is_active.lower() == "true":
                return (
                    super()
                    .get_queryset()
                    .filter(actual_return_date__isnull=True)
                )
            return (
                super().get_queryset().filter(actual_return_date__isnull=False)
            )
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
