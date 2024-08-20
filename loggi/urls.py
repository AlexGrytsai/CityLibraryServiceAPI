from django.urls import path

from loggi.views import LoggingListView

urlpatterns = [
    path("logs/", LoggingListView.as_view(), name="logs")
]

app_name = "loggi"