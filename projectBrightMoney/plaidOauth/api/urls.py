from django.urls import path, re_path

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import refresh_jwt_token

from .views import (
    PlaidPublicTokenView,
    PlaidAccessTokenView,
    PlaidFetchUserTransactionView,
    WebhookTransactionView,
)


urlpatterns = [
    path(
        r"oauth/getPublicToken",
        PlaidPublicTokenView.as_view(),
        name="plaid_public_token",
    ),
    path(
        r"oauth/generateAccessToken",
        PlaidAccessTokenView.as_view(),
        name="plaid_access_token",
    ),
    path(
        r"public/fetchUserTransactions",
        PlaidFetchUserTransactionView.as_view(),
        name="fetch_transactions",
    ),
    path(
        r"public/webhook/receive_transactions",
        WebhookTransactionView.as_view(),
        name="fetch_transactions",
    ),
]

# Add Multiple Format Support
urlpatterns = format_suffix_patterns(urlpatterns)
