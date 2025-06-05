from django.db import models
from job.choices import StatusChoices, ApplicationStatusChoices
import uuid
from core.models import User

class Job(models.Model):
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    location = models.CharField(max_length=50)
    salary = models.PositiveIntegerField()
    deadline = models.DateField()
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")

    def __str__(self):
        return f"Job id = {self.job_id}, Job title = {self.title}, posted by {self.recruiter.first_name}"
    
class JobApplication(models.Model):
    application_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=10, choices=ApplicationStatusChoices.choices, default=ApplicationStatusChoices.APPLIED)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("candidate", "job")

    def __str__(self):
        return f"{self.candidate.email} => {self.job.title}"