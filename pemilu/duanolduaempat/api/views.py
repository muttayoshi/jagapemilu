import json

from django.http import HttpResponse
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from pemilu.duanolduaempat.api.serializers import ReportSerializer
from pemilu.duanolduaempat.models import Report
from pemilu.duanolduaempat.tasks import run_anomaly_detection, run_calculate_province_report
from pemilu.duanolduaempat.utils import calculate_percentage_detail


class UpdateReportDetailView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        run_calculate_province_report.delay()
        return HttpResponse(
            content=json.dumps({"message": "Calculate running in background process"}),
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
        # data = anomaly_detection()
        run_anomaly_detection()
        return HttpResponse(
            content=json.dumps({"message": "Anomaly detection is running"}),
            status=200,
            content_type="application/json",
        )


class ReportViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
