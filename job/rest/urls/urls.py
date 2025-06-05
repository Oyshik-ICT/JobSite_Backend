from django.urls import include, path
from rest_framework.routers import DefaultRouter

from job.rest.views.job import (
    JobApplicationViewSet,
    JobViewSet,
    SpecificRecruiterDashboardAPIView,
)

urlpatterns = [
    path(
        "recruiter-dashboard/",
        SpecificRecruiterDashboardAPIView.as_view(),
        name="recruiter-dashboard",
    ),
]

router = DefaultRouter()
router.register("job", JobViewSet)
router.register("application", JobApplicationViewSet)

urlpatterns += router.urls
