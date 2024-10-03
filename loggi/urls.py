from django.urls import path

from loggi.views import LoggingListAPIView

urlpatterns = [
    path("logs/", LoggingListAPIView.as_view(), name="logs")
]

app_name = "loggi"
