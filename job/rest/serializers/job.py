from job.models import Job
from rest_framework import serializers
from django.utils import timezone

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["job_id", "title", "description", "location", "salary", "deadline", "status", "created_at", "updated_at", "recruiter"]

        extra_kwargs = {"job_id":{"read_only": True}, "created_at":{"read_only": True}, "updated_at":{"read_only": True}, "recruiter":{"read_only": True}}

    def validate_salary(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "salary must be greater than zero"
            )
        
        return value
    
    def validate_deadline(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError(
                "deadline must be a future date"
            )
        return value
    
    def update(self, instance, validated_data):
        update_fields = []

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            update_fields.append(attr)

        instance.save(update_fields=update_fields)

        return instance