from django.urls import path, include

from auth.rest.views.register import UserRegisterView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("register", UserRegisterView)

urlpatterns = router.urls