from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import get_object_or_404

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(
        auto_now_add=True,
        db_comment="Borrowing date of the book",
        help_text="Borrowing date of the book",
    )
    expected_return_date = models.DateField(
        db_comment="Expected return date of the book",
        help_text="Expected return date of the book",
    )
    actual_return_date = models.DateField(
        null=True,
        blank=True,
        db_comment="Actual return date of the book",
        help_text="Actual return date of the book",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,
        db_comment="Book which the user is borrowed",
        help_text="Book",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        db_comment="User who borrowed the book",
        help_text="User",
    )

    def save(self, *args, **kwargs) -> None:
        if self.pk is not None:
            old_instance = get_object_or_404(Borrowing, pk=self.pk)
            if (
                old_instance.actual_return_date
                and old_instance.actual_return_date != self.actual_return_date
            ):
                raise ValidationError(
                    "Cannot change actual_return_date once it is set."
                )
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-expected_return_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["book", "user"], name="unique_borrowing"
            ),
            models.CheckConstraint(
                name="expected_return_date_check",
                check=models.Q(
                    expected_return_date__gte=models.F("borrow_date")
                ),
            ),
        ]

    def __str__(self):
        return f"{self.book.title} borrowed by {self.user}"
