from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser

from borrowing.serializers import BorrowingSerializer


class BorrowingView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAdminUser,)

    def get_serializer_class(self):
        if self.action == 'create':
            return BorrowingSerializer
