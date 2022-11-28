from django.urls import path, include

app_name = "plaidOauth"

urlpatterns = [
    path("api/", include("plaidOauth.api.urls")),
]
