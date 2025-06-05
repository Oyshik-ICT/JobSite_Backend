import logging

from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from auth.permissions import IsCandidate, IsRecruiter
from job.choices import ApplicationStatusChoices, StatusChoices
from job.models import Job, JobApplication
from job.rest.serializers.job import (
    JobApplicationSerializer,
    JobSerializer,
    UpdateJobApplicationSerializer,
)

logger = logging.getLogger(__name__)


class JobViewSet(viewsets.ModelViewSet):
    """Handles job creation and management by recruiters"""

    queryset = Job.objects.select_related("recruiter")
    permission_classes = [IsRecruiter]
    serializer_class = JobSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(recruiter=self.request.user)
        except Exception as e:
            logger.exception(f"Error creating the job: {str(e)}")
            raise ValidationError("Something went wrong while creating the job")


class JobApplicationViewSet(viewsets.ModelViewSet):
    """Handle job applications by candidates and review by recruiters"""

    queryset = JobApplication.objects.select_related("job", "candidate")

    def get_serializer_class(self):
        """Return serializers based on action"""

        if self.action in ["update", "partial_update"]:
            return UpdateJobApplicationSerializer
        else:
            return JobApplicationSerializer

    def get_permissions(self):
        """Assign permission based on action"""

        if self.action == "create":
            self.permission_classes = [IsCandidate]
        else:
            self.permission_classes = [IsRecruiter]
        return super().get_permissions()

    def perform_create(self, serializer):
        try:
            candidate = self.request.user
            job = serializer.validated_data.get("job")

            if JobApplication.objects.filter(candidate=candidate, job=job).exists():
                raise ValidationError("You have already applied for this job")

            serializer.save(candidate=candidate)
        except Exception as e:
            logger.exception(f"Error during job application creation: {str(e)}")
            raise ValidationError("Something wrong while applying to the job")


class SpecificRecruiterDashboardAPIView(APIView):
    """Provide job and application stats for the recruiter"""

    permission_classes = [IsRecruiter]

    def get(self, request):
        """Return recruiter specific dashboard stats"""

        try:
            recruiter = request.user

            total_published_job = Job.objects.filter(recruiter=recruiter).count()
            total_closed_job = Job.objects.filter(
                recruiter=recruiter, status=StatusChoices.CLOSED
            ).count()
            total_candidate_application = JobApplication.objects.filter(
                job__recruiter=recruiter
            ).count()
            total_candidate_hired = JobApplication.objects.filter(
                job__recruiter=recruiter, status=ApplicationStatusChoices.HIRED
            ).count()
            total_candidate_rejected = JobApplication.objects.filter(
                job__recruiter=recruiter, status=ApplicationStatusChoices.REJECTED
            ).count()

            return Response(
                {
                    "total_published_job": total_published_job,
                    "total_closed_job": total_closed_job,
                    "total_candidate_application": total_candidate_application,
                    "total_candidate_hired": total_candidate_hired,
                    "total_candidate_rejected": total_candidate_rejected,
                }
            )
        except Exception as e:
            logger.exception(f"Error retrieving recruiter dashboard: {str(e)}")
            return Response(
                {"details": "Failed to load dashboard data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
