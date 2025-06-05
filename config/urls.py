from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Junior Backend Developer Project Task",
        default_version="v1",
        description="""
This backend project task is designed for junior developer candidates to evaluate their skills in Django and Django REST Framework. The project is a simplified **Job Listing Platform (JobSite)** with user authentication, role-based access, job posting, and application tracking functionalities.

---

### ✅ Initial Setup (Already Done)
- User registration API
- Token authentication using JWT (SimpleJWT)
- Project initialized and uploaded to GitHub

---

### 🚀 Task Breakdown

#### 1. Role-Based User Model
- Add `role` field in `User` model.
- Allowed role choices:
  - `Recruiter`
  - `Candidate`
- Implement role based authorization for different type of roles, also for every endpoint use permission classes except public endpoint.

#### 2. Send Email on Registration
- After successful user registration, send a welcome email to user using `python-decouple`
- Email credentials must be stored securely in `.env`

#### 3. Forgot & Reset Password
- Implement endpoints for:
  - Forgot Password: sends reset link to user’s email
  - Reset Password: allows setting a new password using the reset token

---

### 📂 Job Application Module

#### 4. Job Posting
- Only `Recruiter` users can create, update, or delete jobs
- Job model fields may include:
  -Unique_Job_ID, Title, Description, Location, Salary, Deadline, Status, etc.

#### 5. Job Applications
- Only `Candidate` users can apply to jobs
- Prevent applications:
  - After job deadline
  - Multiple times to the same job by the same candidate

---

### 📊 Recruiter Dashboard Endpoint
Create an endpoint to return the following stats for the logged-in recruiter:

- Total published jobs
- Total closed jobs
- Total candidate applications
- Total candidates hired
- Total candidates rejected

---

### 📌 General Requirements

- Use **Django REST Framework (DRF)** with **class-based views**
- Use **custom permissions** to restrict actions by role
- Clean, paginated, RESTful APIs
- Admin panel must reflect all models
- Use **Swagger/OpenAPI** documentation (drf-yasg)

---

### 🛠️ Instructions for Candidates

1. Clone the GitHub repository provided
2. Set up a virtual environment and install dependencies
3. Follow the existing structure and complete the tasks
4. Use `.env` for sensitive credentials (email, DB, secret keys)

---

### 🎯 Evaluation Criteria

- Code quality and organization
- Proper use of Django & DRF features
- Clean and consistent API structure
- Secure and efficient implementation
- Git commit history and documentation

---

Please write clean, modular, and testable code. Document all your API endpoints properly. Ask questions if anything is unclear.

Good luck! 🚀
"""
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    # Authentication related URLs
    path("api/v1/auth/", include("auth.rest.urls")),
    path("api/v1/job-info/", include("job.rest.urls")),
]

# Add silk profiler urls
urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Swagger urls for API documentation
if settings.ENABLE_SWAGGER:
    urlpatterns += [
        path(
            "swagger<format>/",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),

    ]
