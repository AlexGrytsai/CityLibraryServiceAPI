import logging
from datetime import datetime
from typing import Type

from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import viewsets, mixins, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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

        if user_id:
            if current_user.is_staff:

                logger.info(
                    f"{current_user} used 'user_id'={user_id} "
                    f"for filter borrowed books"
                )
                return super().get_queryset().filter(user__id=user_id)
            else:
                logger.info(
                    f"{current_user} tried to use 'user_id'={user_id} "
                    f"for filter borrowed books"
                )
                return super().get_queryset().none()
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

    @action(
        detail=True,
        methods=["GET"],
        url_path="return",
        url_name="return",
        permission_classes=(IsAdminUser,)
    )
    def return_book(self, request: HttpRequest, pk: int) -> Response:
        borrowing = self.get_object()
        if borrowing.actual_return_date is not None:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Book already returned"}
            )

        borrowing.actual_return_date = datetime.now()

        logger.info(
            f"Inventory until returning: {borrowing.book.inventory}"
        )

        borrowing.book.inventory += 1
        borrowing.book.save()

        logger.info(
            f"Book (id={borrowing.book.id}) returned "
            f"by user id={borrowing.user.id}. "
            f"Inventory={borrowing.book.inventory})"
        )

        borrowing.save()
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message":
                    f"Book {borrowing.book.title} "
                    f"(id={borrowing.book.id}) returned"
            }
        )
