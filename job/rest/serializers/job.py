from django.utils import timezone
from rest_framework import serializers

from job.models import Job, JobApplication


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "job_id",
            "title",
            "description",
            "location",
            "salary",
            "deadline",
            "status",
            "created_at",
            "updated_at",
            "recruiter",
        ]

        extra_kwargs = {
            "job_id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "recruiter": {"read_only": True},
        }

    def validate_salary(self, value):
        if value <= 0:
            raise serializers.ValidationError("salary must be greater than zero")

        return value

    def validate_deadline(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("deadline must be a future date")
        return value

    def update(self, instance, validated_data):
        update_fields = []

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            update_fields.append(attr)

        instance.save(update_fields=update_fields)

        return instance


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["application_id", "job", "candidate", "status", "applied_at"]

        extra_kwargs = {
            "application_id": {"read_only": True},
            "candidate": {"read_only": True},
            "applied_at": {"read_only": True},
            "status": {"read_only": True},
        }


class UpdateJobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["status"]

    def update(self, instance, validated_data):
        instance.save(update_fields=["status"])

        return instance
