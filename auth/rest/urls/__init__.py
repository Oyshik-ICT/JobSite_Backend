from django.urls import path, include


urlpatterns = [
    path("people/", include("auth.rest.urls.register")),
    path("token/", include("auth.rest.urls.token")),
    path("password/", include("auth.rest.urls.password")),
]