from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.serializers import UserCreateSerializer


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
