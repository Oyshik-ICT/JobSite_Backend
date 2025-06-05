from django.db import models

class StatusChoices(models.TextChoices):
    OPEN = "OPEN", "Open"
    CLOSED = "CLOSED", "Closed"

class ApplicationStatusChoices(models.TextChoices):
    APPLIED = "APPLIED", "Applied"
    HIRED = "HIRED", "Hired"
    REJECTED = "REJECTED", "Rejected"