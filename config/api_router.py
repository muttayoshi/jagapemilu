from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from pemilu.duanolduaempat.api.views import ReportViewSet
from pemilu.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("reports", ReportViewSet)

app_name = "api"
urlpatterns = router.urls
