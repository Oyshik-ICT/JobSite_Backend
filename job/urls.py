from django.urls import path, include

from job.rest.views.job import JobViewSet, JobApplicationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("job", JobViewSet)
router.register("application", JobApplicationViewSet)

urlpatterns = router.urls