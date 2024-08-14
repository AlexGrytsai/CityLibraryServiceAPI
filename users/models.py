from __future__ import annotations

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields) -> User:
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email: str, password: str = None, **extra_fields
    ) -> User:
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: str, **extra_fields
    ) -> User:
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    User model that uses email as the username.
    """

    username = models.CharField(
        _("username"), max_length=150, blank=True, null=True
    )

    # Add an email field with a unique constraint.
    email = models.EmailField(_("email address"), unique=True)

    # Set the USERNAME_FIELD to email.
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # Use the custom UserManager.
    objects = UserManager()

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        """String representation of the User model."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.username:
            return self.username
        return self.email

    class Meta:
        ordering = ["email"]
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["last_name", "first_name"]),
            models.Index(fields=["email"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["username"],
                condition=Q(username__isnull=False),
                name="unique_username",
                violation_error_message="A user with that username already "
                "exists.",
            ),
        ]
