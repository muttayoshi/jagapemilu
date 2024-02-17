import json

from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import (
    RetrieveAPIView,
)

from .serializers import PercentageSerializer, DetailSerializer
from pemilu.duanolduaempat.utils import calculate_percentage, calculate_percentage_detail, anomaly_detection
from django.http import FileResponse, HttpResponse


class PercentageView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        data = calculate_percentage()
        return HttpResponse(
            content=json.dumps(data),
            status=200,
            content_type="application/json",
        )

class DetailView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        data = calculate_percentage_detail()
        return HttpResponse(
            content=json.dumps(data),
            status=200,
            content_type="application/json",
        )


class AnomalyDetectionView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        data = anomaly_detection()
        return HttpResponse(
            content=json.dumps(data),
            status=200,
            content_type="application/json",
        )
