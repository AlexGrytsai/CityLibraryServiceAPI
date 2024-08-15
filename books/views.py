from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny

from books.models import Book
from books.serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="List all books",
        tags=["Books"],
        description="Retrieve a list of all books available in the system.",
        responses={200: BookListSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific book",
        tags=["Books"],
        description="Retrieve the details of a specific book by its ID.",
        responses={200: BookSerializer},
    ),
    create=extend_schema(
        summary="Create a new book",
        tags=["Books"],
        description="Create a new book entry. Only accessible to admins.",
        request=BookSerializer,
        responses={201: BookSerializer},
    ),
    update=extend_schema(
        summary="Update a book",
        tags=["Books"],
        description="Update the details of an existing book. "
        "Only accessible to admins.",
        request=BookSerializer,
        responses={200: BookSerializer},
    ),
    partial_update=extend_schema(
        summary="Partially update a book",
        tags=["Books"],
        description="Partially update the details of an existing book. "
        "Only accessible to admins.",
        request=BookSerializer,
        responses={200: BookSerializer},
    ),
    destroy=extend_schema(
        summary="Delete a book",
        tags=["Books"],
        description="Delete a book entry. Only accessible to admins.",
        responses={204: None},
    ),
)
class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions to manage books in the system.
    """

    queryset = Book.objects.all()

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return (IsAdminUser(),)
        return (AllowAny(),)

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        if self.action == "retrieve":
            return BookDetailSerializer
        return BookSerializer

    def get_queryset(self):
        if self.action == "retrieve":
            return Book.objects.filter(id=self.kwargs["pk"])
        return super(BookViewSet, self).get_queryset()
