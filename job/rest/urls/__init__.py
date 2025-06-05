from django.urls import path, include


urlpatterns = [
    path("", include("job.rest.urls.urls")),
]