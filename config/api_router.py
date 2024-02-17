from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from pemilu.users.api.views import UserViewSet
from pemilu.duanolduaempat.api.views import ReportViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("reports", ReportViewSet)

app_name = "api"
urlpatterns = router.urls
