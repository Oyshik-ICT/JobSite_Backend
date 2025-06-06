# 🚀 Job Listing Platform (JobSite)

A comprehensive backend project built with Django and Django REST Framework for managing job postings and applications with role-based authentication.

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Environment Configuration](#-environment-configuration)
- [Running the Server](#-running-the-server)
- [API Documentation](#-api-documentation)
- [Authentication](#-authentication)
- [API Endpoints](#-api-endpoints)
- [User Roles](#-user-roles)
- [Usage Examples](#-usage-examples)

## ⭐ Features

- **User Authentication & Authorization**
  - JWT-based authentication
  - Role-based access control (Recruiter/Candidate)
  - User registration with email verification
  - Password reset functionality

- **Job Management**
  - Job posting by recruiters
  - Job application by candidates
  - Application status tracking
  - Deadline management

- **Dashboard & Analytics**
  - Recruiter dashboard with comprehensive stats
  - Application tracking
  - Job performance metrics

- **Email Notifications**
  - Welcome emails on registration
  - Password reset emails
  - Secure email configuration

## 🛠 Tech Stack

- **Backend**: Django 4.x, Django REST Framework
- **Database**: SQLite
- **Authentication**: JWT (Simple JWT)
- **Documentation**: Swagger/OpenAPI (drf-yasg)
- **Email**: SMTP with Gmail
- **Environment**: python-decouple

## 📋 Prerequisites

Before running this project, make sure you have:

- Python 3.8+
- pip (Python package manager)
- Git
- Virtual environment (recommended)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Oyshik-ICT/JobSite_Backend.git

cd JobSite_Backend
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory and configure the following:

```env
SECRET_KEY=your-secret-key-here

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

```

> **Note**: For Gmail, you need to use an "App Password" instead of your regular password. Enable 2FA and generate an app password from your Google Account settings.

### 5. Database Setup

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

## 🏃‍♂️ Running the Server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`

## 🔐 Authentication

This project uses JWT (JSON Web Token) for authentication.

### 🚨 **IMPORTANT: Authorization Header Format**

> **⚠️ When using JWT tokens for API requests, you MUST include the `BEARER` keyword in the Authorization header:**
> 
> ```
> Authorization: BEARER <your-jwt-token>
> ```
> 
> **Example:**
> ```
> Authorization: BEARER eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
> ```

### Getting JWT Token

1. **Register a user** or **login** to get access token
2. **Include the token** in all authenticated requests
3. **Refresh token** when expired

## 📡 API Endpoints

### 🔑 Authentication Endpoints

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| `POST` | `/api/v1/auth/people/register/` | User registration | Public |
| `POST` | `/api/v1/auth/token/` | Login (Get JWT token) | Public |
| `POST` | `/api/v1/auth/token/refresh/` | Refresh JWT token | Public |
| `POST` | `/api/v1/auth/password/forget-password/` | Send password reset email | Authenticated |
| `POST` | `/api/v1/auth/password/reset-password/` | Reset password with token | Public |

### 👥 User Management

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| `GET` | `/api/v1/auth/people/register/` | List users (filtered by role) | Authenticated |
| `GET` | `/api/v1/auth/people/register/{id}/` | Get user details | Authenticated |
| `PUT` | `/api/v1/auth/people/register/{id}/` | Update user | Authenticated |
| `DELETE` | `/api/v1/auth/people/register/{id}/` | Delete user | Authenticated |

### 💼 Job Management

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| `GET` | `/api/v1/job-info/job/` | List all jobs | Recruiter |
| `POST` | `/api/v1/job-info/job/` | Create new job | Recruiter |
| `GET` | `/api/v1/job-info/job/{id}/` | Get job details | Recruiter |
| `PUT` | `/api/v1/job-info/job/{id}/` | Update job | Recruiter |
| `DELETE` | `/api/v1/job-info/job/{id}/` | Delete job | Recruiter |

### 📝 Job Applications

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| `GET` | `/api/v1/job-info/application/` | List applications | Recruiter |
| `POST` | `/api/v1/job-info/application/` | Apply to job | Candidate |
| `GET` | `/api/v1/job-info/application/{id}/` | Get application details | Recruiter |
| `PATCH` | `/api/v1/job-info/application/{id}/` | Update application status | Recruiter |

### 📊 Dashboard

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| `GET` | `/api/v1/job-info/recruiter-dashboard/` | Get recruiter statistics | Recruiter |

## 👤 User Roles

### 🏢 Recruiter
- Create, update, delete job postings
- View and manage job applications
- Update application status (hired/rejected)
- Access recruiter dashboard with analytics

### 🎯 Candidate
- View available job listings
- Apply to jobs (once per job)
- Cannot apply after job deadline
- Cannot apply to closed jobs

## 💡 Usage Examples

### 1. User Registration

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/people/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepass123",
    "confirm_password": "securepass123",
    "role": "CANDIDATE"
  }'
```

### 2. Login & Get Token

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

### 3. Create Job (Recruiter)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/job-info/job/ \
  -H "Content-Type: application/json" \
  -H "Authorization: BEARER <your-jwt-token>" \
  -d '{
    "title": "Senior Python Developer",
    "description": "We are looking for an experienced Python developer...",
    "location": "Remote",
    "salary": 75000,
    "deadline": "2024-12-31"
  }'
```

### 4. Apply to Job (Candidate)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/job-info/application/ \
  -H "Content-Type: application/json" \
  -H "Authorization: BEARER <your-jwt-token>" \
  -d '{
    "job": "job-uuid-here"
  }'
```


## 🔧 Key Features Explained

### Role-Based Permissions
- **IsRecruiter**: Only recruiters can create/manage jobs
- **IsCandidate**: Only candidates can apply to jobs
- **IsRecruiterOrCandidateOrAdmin**: Both roles can access certain endpoints

### Email Integration
- Welcome email sent after successful registration
- Password reset emails with secure tokens
- SMTP configuration with Gmail

### Job Application Logic
- Prevents duplicate applications
- Blocks applications after deadline
- Prevents applications to closed jobs

### Dashboard Analytics
- Total published jobs
- Total closed jobs
- Total candidate applications
- Total candidates hired
- Total candidates rejected

## 🐛 Troubleshooting

### Common Issues

1. **Email not sending**: Check your Gmail app password and 2FA settings
2. **Token authentication failing**: Ensure you're using `BEARER` prefix
3. **Permission denied**: Verify user role and endpoint permissions
4. **Database errors**: Run migrations with `python manage.py migrate`

### Debug Mode

Set `DEBUG=True` in your `.env` file for detailed error messages during development.

