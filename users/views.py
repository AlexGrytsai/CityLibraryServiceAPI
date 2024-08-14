from typing import Type

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import Serializer

from users.models import User
from users.serializers import (
    UserCreateSerializer,
    UserManageSerializer,
    UserUpdateSerializer,
    UserPasswordUpdateSerializer,
)


@extend_schema(
    summary="Create a new user",
    tags=["Users"],
    description="Register a new user in the system.",
    responses={201: UserCreateSerializer},
)
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


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve current user",
        tags=["Users"],
        description="Fetch the currently authenticated user's details.",
        responses={200: UserManageSerializer},
    ),
    put=extend_schema(
        summary="Update current user details",
        tags=["Users"],
        description="Update the details of the currently authenticated user.",
        request=UserUpdateSerializer,
        responses={200: UserUpdateSerializer},
    ),
    patch=extend_schema(
        summary="Partially update current user details",
        tags=["Users"],
        description="Partially update the details of the currently authenticated user.",
        request=UserUpdateSerializer,
        responses={200: UserUpdateSerializer},
    ),
    delete=extend_schema(
        summary="Delete current user",
        tags=["Users"],
        description="Delete the currently authenticated user.",
        responses={204: None},
    ),
)
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


@extend_schema(
    summary="Update user password",
    tags=["Users"],
    description="Allows the authenticated user to update their password.",
    request=UserPasswordUpdateSerializer,
    responses={200: None},
)
class UserPasswordUpdateView(generics.UpdateAPIView):
    """
    A class-based view for updating a user's password.

    This view handles PUT requests for updating a user's password.
    It requires the user to be authenticated.
    """

    serializer_class = UserPasswordUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user
