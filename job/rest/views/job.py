from job.models import Job
from job.rest.serializers.job import JobSerializer
from rest_framework import viewsets
from auth.permissions import IsRecruiter

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.select_related("recruiter")
    permission_classes = [IsRecruiter]
    serializer_class = JobSerializer

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)
