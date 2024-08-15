from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    class Cover(models.TextChoices):
        HARD = "HARD"
        SOFT = "SOFT"

    title = models.CharField(
        max_length=255,
        unique=True,
        db_comment="Book title",
        help_text="Book title",
    )
    author = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_comment="Book author",
        help_text="Book author",
    )
    cover = models.CharField(
        max_length=5,
        choices=Cover.choices,
        db_comment="Book cover",
        help_text="Book cover",
    )
    inventory = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        db_comment="Book inventory",
        help_text="Book inventory",
    )
    daily_fee = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        db_comment="Book daily fee",
        help_text="Book daily fee",
        validators=[MinValueValidator(0.0)],
    )

    class Meta:
        ordering = ["title", "author"]

    def __str__(self):
        return f"{self.title} by {self.author}"
