from django.urls import path

from pemilu.duanolduaempat.api.views import AnomalyDetectionView, DetailView, UpdateReportDetailView, StartCrawlingView

app_name = "realcount"


urlpatterns = [
    path("update-report", UpdateReportDetailView.as_view(), name="dashboard"),
    path("detail", DetailView.as_view(), name="detail"),
    path("anomaly", AnomalyDetectionView.as_view(), name="anomaly"),
    path("start-crawling/<int:id>", StartCrawlingView.as_view(), name="start-crawling"),
]
