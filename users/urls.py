from django.urls import path

from users.views import UserCreateView, ManageUserView

urlpatterns = [
    path("", UserCreateView.as_view(), name="register"),
    path("me/", ManageUserView.as_view(), name="me"),
]
