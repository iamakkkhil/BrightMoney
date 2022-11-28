from django.contrib import admin
from django.urls import path, include

# from utils.plaid import client

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("plaid/", include("plaidOauth.urls")),
    # path('api-auth/', include('rest_framework.urls'))
]
