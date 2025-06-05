from django.db import models
from job.choices import StatusChoices
import uuid
from core.models import User

class Job(models.Model):
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=50)
    salary = models.PositiveIntegerField()
    deadline = models.DateField()
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")

    def __str__(self):
        return f"Job id = {self.job_id}, posted by {self.recruiter.first_name}"