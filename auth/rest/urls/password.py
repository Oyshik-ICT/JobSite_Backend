from django.urls import path
from auth.rest.views.register import ForgetPasswordAPIView, ResetPasswordAPIView



urlpatterns = [
    path("forget-password/", ForgetPasswordAPIView.as_view(), name="forget-password"),
    path("reset-password/", ResetPasswordAPIView.as_view(), name="reset-password"),
]
