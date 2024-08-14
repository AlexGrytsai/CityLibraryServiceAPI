from typing import Type

from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import Serializer

from users.models import User
from users.serializers import UserCreateSerializer, UserManageSerializer, \
    UserUpdateSerializer


class UserCreateView(generics.CreateAPIView):
    """
    UserCreateView is a class-based view that inherits from
    generics.CreateAPIView.
    It is used to handle the creation of new User instances.

    This view uses the UserCreateSerializer to validate and serialize
    the data from the request.
    It allows any user to create a new User instance, as specified
    by the AllowAny permission class.
    """

    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """
    A class-based view for managing user instances.

    This view handles GET, PUT, and DELETE requests for user instances.
    It requires the user to be authenticated.
    """

    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        user = self.request.user

        return User.objects.all().filter(id=user.id)

    def get_object(self) -> User:
        return self.request.user

    def get_serializer_class(self) -> Type[Serializer]:
        if self.request.method == "GET":
            return UserManageSerializer
        return UserUpdateSerializer
