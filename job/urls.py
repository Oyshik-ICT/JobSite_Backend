from django.urls import path, include

from job.rest.views.job import JobViewSet, JobApplicationViewSet, SpecificRecruiterDashboardAPIView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("recruiter-dashboard/", SpecificRecruiterDashboardAPIView.as_view(), name="recruiter-dashboard"),
]

router = DefaultRouter()
router.register("job", JobViewSet)
router.register("application", JobApplicationViewSet)

urlpatterns += router.urls