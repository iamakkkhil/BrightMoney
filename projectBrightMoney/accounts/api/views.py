from rest_framework import status, permissions, views
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from utils.functions import blacklist_tokens
from rest_framework_simplejwt.tokens import RefreshToken
from utils.serializers import (
    get_tokens_for_user,
)

from utils.permissions import IsAuthenticated

from .serializers import (
    UserLoginSerializer,
    UserSignupSerializer,
)


class UserLoginView(RetrieveAPIView):
    """
    API endpoint that allows users to login.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            "success": "True",
            "message": "User logged in successfully",
            "access_token": serializer.validated_data["tokens"]["access"],
            "refresh_token": serializer.validated_data["tokens"]["refresh"],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class UserSignupView(CreateAPIView):
    """
    API endpoint that allows users to signup.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSignupSerializer

    def create(self, request):
        """
        Signing up new user
        """
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "success": "True",
            "message": "User created successfully",
        }

        return Response(response, status=status.HTTP_200_OK)


class LogoutView(views.APIView):
    """
    View for logging out a user
    """

    # throttle_scope = "user"
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        POST request to logout a user
        """

        refresh_token = request.data.get("refresh_token")
        blacklist_current_refresh_token = blacklist_tokens(refresh_token)

        if blacklist_current_refresh_token:
            response = {
                "success": "True",
                "message": "User logged out successfully",
            }
            status_code = status.HTTP_200_OK
        else:
            response = {
                "success": "False",
                "message": "User not logged out",
            }
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(response, status=status_code)


class TokenRefreshNewView(views.APIView):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        refresh_token = request.data.get("refresh_token")
        print(refresh_token)

        try:
            refresh_token = RefreshToken(refresh_token)
            print("refresh_token new", refresh_token)
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        token = get_tokens_for_user(user)

        response = {"success": "True", "token": token["access"]}
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)
