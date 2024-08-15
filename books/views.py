from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny

from books.models import Book
from books.serializers import BookSerializer, BookListSerializer


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
        return BookSerializer

    def get_queryset(self):
        if self.action == "retrieve":
            return Book.objects.filter(id=self.kwargs["pk"])
        return super(BookViewSet, self).get_queryset()
