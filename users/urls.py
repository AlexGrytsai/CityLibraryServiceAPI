from django.urls import path

from users.views import UserCreateView, ManageUserView, UserPasswordUpdateView

urlpatterns = [
    path("", UserCreateView.as_view(), name="register"),
    path("me/", ManageUserView.as_view(), name="me"),
    path(
        "me/update-password/",
        UserPasswordUpdateView.as_view(),
        name="update-password",
    ),
]
