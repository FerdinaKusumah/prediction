import json
from typing import Callable

from auditlog.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from prediction.serializer.history import HistoryModelSerializer


def error_404_view(request, *args, **argv):
    return HttpResponse(
        json.dumps(
            {"status": status.HTTP_404_NOT_FOUND, "message": "Object is not exists"}
        ),
        content_type="application/json",
    )


def error_500_view(request, *args, **argv):
    return HttpResponse(
        json.dumps(
            {
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Something went wrong",
            }
        ),
        content_type="application/json",
    )


class BaseViewSet(viewsets.ModelViewSet):
    @staticmethod
    def response_success(data: dict[str, any] = None):
        resp = {"status": status.HTTP_200_OK}
        if data is not None:
            resp["data"] = data

        return Response(resp, status=status.HTTP_200_OK)

    @staticmethod
    def response_bad_request(message: dict[str, any] | str = None):
        resp = {"status": status.HTTP_400_BAD_REQUEST}
        if message is not None:
            resp["message"] = message

        return Response(resp, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def response_no_content():
        return Response(status=status.HTTP_204_NO_CONTENT)

    def history_module(self, model: Callable):
        """Get history module from model"""
        obj = ContentType.objects.get_for_model(model)
        query = LogEntry.objects.filter(content_type_id=obj.id).all()
        queryset = self.filter_queryset(query)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = HistoryModelSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
        else:
            serializer = HistoryModelSerializer(queryset, many=True)
            data = serializer.data

        # return response
        return self.response_success(data)
