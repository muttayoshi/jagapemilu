import json

from django.http import HttpResponse
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from pemilu.duanolduaempat.api.serializers import ReportSerializer
from pemilu.duanolduaempat.models import Report
from pemilu.duanolduaempat.tasks import run_anomaly_detection, run_calculate_province_report, crawling_select_province, \
    run_calculate_provice_anomaly_tps_report, crawling_server_1, crawling_server_2, crawling_server_3, crawling_server_4
from pemilu.duanolduaempat.utils import calculate_percentage_detail


class UpdateReportDetailView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        run_calculate_province_report.delay()
        run_calculate_provice_anomaly_tps_report.delay()
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


class StartCrawlingView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        server = kwargs.get("id")
        if server == 1:
            crawling_server_1()
        elif server == 2:
            crawling_server_2()
        elif server == 3:
            crawling_server_3()
        elif server == 4:
            crawling_server_4()
        return HttpResponse(
            content=json.dumps({"message": "Crawling is running in background process"}),
            status=200,
            content_type="application/json",
        )
