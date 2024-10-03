from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from safety.auth.cli import status

from loggi.models import Log


class LoggingListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {"detail": "Not authorized"},
                status=status.HTTP_403_FORBIDDEN
            )
        paginator = LimitOffsetPagination()
        logs = Log

        logs_list = []

        for pk in logs.all_pks():
            log = dict(logs.get(pk))
            del log["pk"]
            logs_list.append(log)
        logs_list.sort(key=lambda x: x["data_time"], reverse=True)
        paginated_logs = paginator.paginate_queryset(
            logs_list, request, view=self
        )

        return paginator.get_paginated_response(paginated_logs)
