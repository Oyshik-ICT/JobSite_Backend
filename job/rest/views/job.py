from job.models import Job, JobApplication
from job.rest.serializers.job import JobSerializer, JobApplicationSerializer, UpdateJobApplicationSerializer
from rest_framework import viewsets
from auth.permissions import IsRecruiter, IsCandidate
from rest_framework.exceptions import ValidationError

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.select_related("recruiter")
    permission_classes = [IsRecruiter]
    serializer_class = JobSerializer

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.select_related("job", "candidate")

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UpdateJobApplicationSerializer
        else:
            return JobApplicationSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsCandidate]
        else:
            self.permission_classes = [IsRecruiter]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        candidate = self.request.user
        job = serializer.validated_data.get("job")

        if JobApplication.objects.filter(candidate=candidate, job=job).exists():
            raise ValidationError("You have already applied for this job")
        
        serializer.save(candidate=candidate)
