from django.urls import path
from borrowing.views import BorrowingView

urlpatterns = [
    path("", BorrowingView.as_view({"post": "create"}), name="borrowing"),
]

app_name = "borrowing"
