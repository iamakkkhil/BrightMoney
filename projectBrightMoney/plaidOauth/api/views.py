from rest_framework import status, permissions, views, generics
from rest_framework.response import Response
from plaidOauth.api.serializers import PlaidAccessTokenSerializer
from plaidOauth.models import PlaidCredentials
from utils.functions import saved_retrieved_accounts_db, get_saved_accounts
from utils.permissions import IsAuthenticated
from utils.plaidApiClient import client
from utils.plaidUtils import (
    create_link_token,
    get_access_token,
    retrieve_transactions,
    fire_test_event,
)
from accounts.models import User
from plaidOauth.models import Account


class PlaidPublicTokenView(views.APIView):
    # throttle_scope = "user"
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        _status, response = create_link_token(client, str(user.id))

        if _status == "failed":
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


class PlaidAccessTokenView(generics.CreateAPIView):
    # throttle_scope = "user"
    permission_classes = (IsAuthenticated,)
    serializer_class = PlaidAccessTokenSerializer

    def post(self, request):
        data = request.data
        token = data.get("token", None)
        if not token:
            return Response(
                {"error": "token parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user

        _status, response = get_access_token(client, token)

        if _status != "success":
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response["id"] = user.id
        if PlaidCredentials.objects.filter(id=response["id"]).exists():
            PlaidCredentials.objects.filter(id=response["id"]).update(
                access_token=response["access_token"],
                item_id=response["item_id"],
                request_id=response["request_id"],
            )
        else:
            serializer = PlaidAccessTokenSerializer(data=response)
            try:
                serializer.is_valid(raise_exception=True)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

        user_id = user.id
        fire_test_event(client, response["access_token"])
        saved_retrieved_accounts_db.delay(
            access_token=response["access_token"], user_id=user_id
        )

        status_code = status.HTTP_200_OK
        return Response({"success": True}, status=status_code)


class PlaidFetchUserTransactionView(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        email = data.get("email", None)
        if not email:
            return Response(
                {"error": "email parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(email=email)
        if not user:
            return Response(
                {"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        plaid_obj_exists = PlaidCredentials.objects.filter(id=user.id).exists()
        if not plaid_obj_exists:
            return Response(
                {"error": "Plaid credentials does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        plaid_obj_token = PlaidCredentials.objects.get(id=user.id)
        plaid_obj_token.access_token
        _status, transaction_response = retrieve_transactions(
            client, plaid_obj_token.access_token
        )
        if _status != "success":
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        accounts = get_saved_accounts(user=user)

        status_code = status.HTTP_200_OK
        response = {
            "success": True,
            "accounts": accounts,
            "transactions": transaction_response,
        }
        return Response(response, status=status_code)


class WebhookTransactionView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data

        status_code = status.HTTP_200_OK
        response = {"success": True, "data": data}
        return Response(response, status=status_code)
