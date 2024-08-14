from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """
    A serializer for creating new user instances.

    This serializer validates user input data and creates a new user instance
    with the provided email, password, username, first name, and last name.
    """

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "username",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,
                "max_length": 128,
                "validators": [validate_password],
                "style": {"input_type": "password", "placeholder": "Password"},
            },
            "username": {
                "required": False,
                "style": {
                    "input_type": "text",
                    "placeholder": "Username (optional)",
                },
            },
            "first_name": {
                "required": False,
                "style": {
                    "input_type": "text",
                    "placeholder": "First Name (optional)",
                },
            },
            "last_name": {
                "required": False,
                "style": {
                    "input_type": "text",
                    "placeholder": "Last Name (optional)",
                },
            },
        }


class UserManageSerializer(serializers.ModelSerializer):
    """
    A serializer for managing user instances.

    This serializer provides a way to serialize and deserialize user data,
    including their ID, email, username, staff status, first name, and last name.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "is_staff",
            "first_name",
            "last_name",
        ]
        read_only_fields = ["id", "is_staff"]
