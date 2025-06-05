from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from auth.permissions import IsRecruiter, IsCandidate, IsRecruiterOrCandidateOrAdmin
from core.models import User
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from auth.rest.serializers.register import UserRegisterSerializer, ResetPasswordSerializer, ForgetPasswordSerializer


class UserRegisterView(viewsets.ModelViewSet):
    """User registration view"""
    
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsRecruiterOrCandidateOrAdmin]
        return super().get_permissions()
    
    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if not user.is_staff and user.role != "RECRUITER":
            qs = qs.filter(email=user.email)
        return qs
    
    def perform_create(self, serializer):
        user = serializer.save()

        send_mail(
            subject="Welcome to our site!",
            message=f"Hi {user.first_name},\n\nThanks for registering",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

class ForgetPasswordAPIView(APIView):
    permission_classes = [IsRecruiterOrCandidateOrAdmin]

    @swagger_auto_schema(request_body=ForgetPasswordSerializer)
    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            email = request.data.get("email")
            user = User.objects.get(email=email, pk=self.request.user.id)
        except User.DoesNotExist:
            return Response(
                {"details": "User Doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            
            )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_url = f"http://127.0.0.1:8000/api/v1/auth/password/reset-password/?uid={uid}&token={token}"

        send_mail(
            subject="Reset your password",
            message=f"Click the link to reset password => {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return Response(
            {"details": "Password reset link sent to your email"},
            status=status.HTTP_200_OK
            
        )

class ResetPasswordAPIView(APIView):

    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        manual_parameters=[
            openapi.Parameter(
                name="uid",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Base64 encoded user ID"
            ),
            openapi.Parameter(
                name="token",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Password reset token"
            )
        ]
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
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response(
                {"details": "Invalid user ID"},
                status=status.HTTP_400_BAD_REQUEST
            
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"details": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            
            )
        
        user.set_password(new_password)
        user.save(update_fields=["password"])
        return Response(
            {"details": "Password reset successful"},
            status=status.HTTP_200_OK
            
        )
