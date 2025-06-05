import logging

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from auth.permissions import IsRecruiterOrCandidateOrAdmin
from auth.rest.serializers.register import (
    ForgetPasswordSerializer,
    ResetPasswordSerializer,
    UserRegisterSerializer,
)
from core.models import User

logger = logging.getLogger(__name__)


class UserRegisterView(viewsets.ModelViewSet):
    """User registration view"""

    queryset = User.objects.order_by("id")
    serializer_class = UserRegisterSerializer

    def get_permissions(self):
        """Assign permission based on action"""

        if self.action == "create":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsRecruiterOrCandidateOrAdmin]
        return super().get_permissions()

    def get_queryset(self):
        """Filter queryset based on role"""
        if getattr(self, "swagger_fake_view", False):
            return User.objects.none()
        
        user = self.request.user
        qs = super().get_queryset()
        if not user.is_staff and getattr(user, 'role', None) != "RECRUITER":
            qs = qs.filter(email=user.email)
        return qs

    def perform_create(self, serializer):
        """Create user and send welcome mail"""
        try:
            user = serializer.save()

            send_mail(
                subject="Welcome to our site!",
                message=f"Hi {user.first_name},\n\nThanks for registering",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.exception(f"Failed to send email during registration: {str(e)}")


class ForgetPasswordAPIView(APIView):
    """Send password reset link to user's email"""

    permission_classes = [IsRecruiterOrCandidateOrAdmin]

    @swagger_auto_schema(request_body=ForgetPasswordSerializer)
    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            email = request.data.get("email")
            user = User.objects.get(email=email, pk=self.request.user.id)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_url = f"http://127.0.0.1:8000/api/v1/auth/password/reset-password/?uid={uid}&token={token}"

            send_mail(
                subject="Reset your password",
                message=f"Click the link to reset password => {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            return Response(
                {"details": "Password reset link sent to your email"},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            logger.warning("User doesn't exist")
            return Response(
                {"details": "User Doesn't exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(f"Failed to send password reset link: {str(e)}")
            return Response(
                {"details": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ResetPasswordAPIView(APIView):
    """Reset user password using token and uid"""

    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        manual_parameters=[
            openapi.Parameter(
                name="uid",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Base64 encoded user ID",
            ),
            openapi.Parameter(
                name="token",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Password reset token",
            ),
        ],
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid64 = request.query_params.get("uid")
        token = request.query_params.get("token")
        new_password = request.data.get("new_password")

        try:
            uid = force_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(pk=uid)

            if not default_token_generator.check_token(user, token):
                return Response(
                    {"details": "Invalid or expired token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(new_password)
            user.save(update_fields=["password"])
            return Response(
                {"details": "Password reset successful"}, status=status.HTTP_200_OK
            )
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response(
                {"details": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(f"Password reset failed: {str(e)}")
            return Response(
                {"details": "Invalid user ID"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
