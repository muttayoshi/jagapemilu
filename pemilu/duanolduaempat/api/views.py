import json

from django.http import HttpResponse
from rest_framework.generics import RetrieveAPIView

from pemilu.duanolduaempat.utils import anomaly_detection, calculate_percentage, calculate_percentage_detail


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
