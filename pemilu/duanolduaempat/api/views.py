import json

from django.http import HttpResponse
from rest_framework.generics import RetrieveAPIView

from pemilu.duanolduaempat.utils import anomaly_detection, calculate_percentage, calculate_percentage_detail
from pemilu.duanolduaempat.api.serializers import ReportSerializer
from pemilu.duanolduaempat.models import Report
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

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


class ReportViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
