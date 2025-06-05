from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from core.models import User, UserProfile


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""

    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "uid",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "password",
            "confirm_password",
        ]

    def validate_password(self, value):
        """Validate the password"""
        # Check length of password
        if len(value) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters long"
            )
        # Check password match with confirm password
        if value != self.initial_data.get("confirm_password"):
            raise serializers.ValidationError(
                "Password and confirm password don't match"
            )
        return value

    def create(self, validated_data):
        """Create a new user"""
        # Remove confirm_password from validated_data
        validated_data.pop("confirm_password", None)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        update_fields = []
        validated_data.pop("confirm_password", None)
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            update_fields.append(attr)

        instance.save(update_fields=update_fields)

        return instance


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        if len(new_password) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters long"
            )
        if new_password != confirm_password:
            raise serializers.ValidationError(
                "Password and confirm password don't match"
            )

        return data
