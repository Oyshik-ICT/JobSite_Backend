from django.contrib.auth.base_user import  AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from core.choices import GenderChoices, UserRole
from core.managers import UserManager

from shared.base_model import BaseModel



class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(max_length=50, unique=True, db_index=True)
    password = models.CharField(max_length=128, blank=True)
    new_password = models.CharField(max_length=128, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=12, choices=UserRole.choices, default=UserRole.CANDIDATE)

    # Add user custom manager
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"uid:{self.uid} {self.email}"

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.password:
                raise ValueError("Password is required")
            self.password = make_password(self.password)
            self.username = self.email if not self.username else self.username

        if self.new_password:
            self.password = make_password(self.new_password)
            self.new_password = ""

        super().save(*args, **kwargs)


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(upload_to="profile_pictures/", blank=True)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=20, choices=GenderChoices.choices, default=GenderChoices.NOT_SET
    )

    def __str__(self):
        return f"Profile of {self.user.email}"
