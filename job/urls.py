from django.urls import path, include

from job.rest.views.job import JobViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("job", JobViewSet)

urlpatterns = router.urls