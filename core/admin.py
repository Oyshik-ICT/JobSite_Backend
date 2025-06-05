from django.contrib import admin

from core.models import User, UserProfile
from job.models import Job, JobApplication

from shared.base_admin import BaseModelAdmin


@admin.register(User)
class UserAdmin(BaseModelAdmin):
    model = User
    list_display = ["uid", "email", "last_login"]

    fieldsets = (
        (None, {"fields": ("email", "password", "new_password")}),
        (
            "Other",
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "phone",
                    "uid",
                    "last_login",
                    "status",
                    "is_staff",
                    "is_superuser",
                    "role"
                ),
            },
        ),
    )

    list_filter = [
        "status",
        "last_login",
    ]

    search_fields = ("phone", "email")
    readonly_fields = BaseModelAdmin.readonly_fields + [
        "last_login",
    ]
    list_select_related = True
    show_full_result_count = False
    ordering = ("-created_at",)


@admin.register(UserProfile)
class UserProfileAdmin(BaseModelAdmin):
    model = UserProfile
    list_display = [
        "user",
        "photo",
        "bio",
        "date_of_birth",
        "gender",
    ]

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    model = Job
    list_display = [
        "job_id",
        "title",
        "recruiter",
        "location",
        "salary",
        "status",
        "deadline",
        "created_at",
    ]
    
    fieldsets = (
        (None, {
            "fields": (
                "title",
                "description",
                "recruiter",
                "location",
                "salary",
                "deadline",
                "status",
            )
        }),
        (
            "Metadata",
            {
                "fields": (
                    "job_id",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
    
    list_filter = [
        "status",
        "location",
        "deadline",
        "created_at",
    ]
    
    search_fields = ("title", "description", "location", "recruiter__email")
    readonly_fields = [
        "job_id",
        "created_at",
        "updated_at",
    ]
    list_select_related = ["recruiter"]
    show_full_result_count = False
    ordering = ("-created_at",)

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication
    list_display = [
        "application_id",
        "candidate",
        "job",
        "status",
        "applied_at",
    ]
    
    fieldsets = (
        (None, {
            "fields": (
                "candidate",
                "job",
                "status",
            )
        }),
        (
            "Metadata",
            {
                "fields": (
                    "application_id",
                    "applied_at",
                ),
            },
        ),
    )
    
    list_filter = [
        "status",
        "applied_at",
        "job__title",
    ]
    
    search_fields = (
        "candidate__email", 
        "candidate__first_name", 
        "candidate__last_name",
        "job__title",
    )
    
    readonly_fields = [
        "application_id",
        "applied_at",
    ]
    
    list_select_related = ["candidate", "job"]
    show_full_result_count = False
    ordering = ("-applied_at",)