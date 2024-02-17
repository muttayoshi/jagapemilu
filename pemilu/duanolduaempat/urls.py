from django.urls import path
from pemilu.duanolduaempat.api.views import PercentageView, DetailView, AnomalyDetectionView


app_name = "realcount"


urlpatterns = [
    path("result", PercentageView.as_view(), name="dashboard"),
    path("detail", DetailView.as_view(), name="detail"),
    path("anomaly", AnomalyDetectionView.as_view(), name="anomaly"),
]
