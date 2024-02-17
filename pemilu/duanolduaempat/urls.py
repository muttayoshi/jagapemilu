from django.urls import path

from pemilu.duanolduaempat.api.views import AnomalyDetectionView, DetailView, PercentageView, ReportViewSet

app_name = "realcount"


urlpatterns = [
    path("result", PercentageView.as_view(), name="dashboard"),
    path("detail", DetailView.as_view(), name="detail"),
    path("anomaly", AnomalyDetectionView.as_view(), name="anomaly"),
    # path("report", ReportView, name="report"),
]
