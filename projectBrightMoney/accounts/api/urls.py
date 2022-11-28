from django.urls import path, re_path

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import refresh_jwt_token

from .views import LogoutView, TokenRefreshNewView, UserLoginView, UserSignupView


urlpatterns = [
    path(r"login", UserLoginView.as_view(), name="user_login"),
    path(r"signup", UserSignupView.as_view(), name="user_signup"),
    path(r"logout", LogoutView.as_view(), name="user_logout"),
    # re_path(r'^api-token-refresh', refresh_jwt_token),
    path("token/refresh/", TokenRefreshNewView.as_view(), name="token-refresh-new"),
]

# Add Multiple Format Support
urlpatterns = format_suffix_patterns(urlpatterns)
