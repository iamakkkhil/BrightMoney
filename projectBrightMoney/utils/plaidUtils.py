import plaid
import json
import datetime
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,
)
from plaid.model.item_webhook_update_request import ItemWebhookUpdateRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.sandbox_item_fire_webhook_request import SandboxItemFireWebhookRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode


def create_link_token(client, client_user_id):
    try:
        request = LinkTokenCreateRequest(
            products=[Products("auth"), Products("transactions")],
            client_name="Plaid Test App",
            country_codes=[CountryCode("US")],
            language="en",
            user=LinkTokenCreateRequestUser(client_user_id=client_user_id),
            # redirect_uri='http://localhost:5173/',
            # webhook='https://sample-webhook-uri.com',
        )
        response = client.link_token_create(request)
        # Send the data to the client
        return "success", response.to_dict()

    except plaid.ApiException as e:
        response = json.loads(e.body)
        return "failed", response


def get_access_token(client, public_token):
    try:
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = client.item_public_token_exchange(request)
        return "success", response.to_dict()

    except plaid.ApiException as e:
        response = json.loads(e.body)
        return "failed", response


def format_transactions(transactions):
    transactions_list = list()
    for transaction in transactions:
        transactions_list.append(
            {
                "account_id": transaction.get("account_id", None),
                "account_owner": transaction.get("account_owner", None),
                "amount": transaction.get("amount", None),
                "authorized_date": transaction.get("authorized_date", None),
                "authorized_date_time": transaction.get("authorized_date_time", None),
                "category": transaction.get("category", None),
                "category_id": transaction.get("category_id", None),
                "check_number": transaction.get("check_number", None),
                "date": transaction.get("date", None),
                "datetime": transaction.get("datetime", None),
                "iso_currency_code": transaction.get("iso_currency_code", None),
                "location": {
                    "address": transaction.get("location", {}).get("address", None),
                    "city": transaction.get("location", {}).get("city", None),
                    "country": transaction.get("location", {}).get("country", None),
                    "lat": transaction.get("location", {}).get("lat", None),
                    "lon": transaction.get("location", {}).get("lon", None),
                    "postal_code": transaction.get("location", {}).get(
                        "postal_code", None
                    ),
                    "region": transaction.get("location", {}).get("region", None),
                    "store_number": transaction.get("location", {}).get(
                        "store_number", None
                    ),
                },
                "merchant_name": transaction.get("merchant_name", None),
                "name": transaction.get("name", None),
                "payment_channel": transaction.get("payment_channel", None),
                "payment_meta": {
                    "by_order_of": transaction.get("payment_meta", {}).get(
                        "by_order_of", None
                    ),
                    "payee": transaction.get("payment_meta", {}).get("payee", None),
                    "payer": transaction.get("payment_meta", {}).get("payer", None),
                    "payment_method": transaction.get("payment_meta", {}).get(
                        "payment_method", None
                    ),
                    "payment_processor": transaction.get("payment_meta", {}).get(
                        "payment_processor", None
                    ),
                    "ppd_id": transaction.get("payment_meta", {}).get("ppd_id", None),
                    "reason": transaction.get("payment_meta", {}).get("reason", None),
                    "reference_number": transaction.get("payment_meta", {}).get(
                        "reference_number", None
                    ),
                },
                "pending": transaction.get("pending", None),
                "pending_transaction_id": transaction.get(
                    "pending_transaction_id", None
                ),
                "personal_finance_category": transaction.get(
                    "personal_finance_category", None
                ),
                "transaction_code": transaction.get("transaction_code", None),
                "transaction_code": transaction.get("transaction_code", None),
                "transaction_id": transaction.get("transaction_id", None),
                "transaction_type": transaction.get("transaction_type", None),
                "unofficial_currency_code": transaction.get(
                    "unofficial_currency_code", None
                ),
            }
        )
    return transactions_list


# @shared_task
def retrieve_accounts(client, access_token):
    try:
        request = AccountsGetRequest(access_token=access_token)
        response = client.accounts_get(request)
        return "success", response.to_dict()

    except plaid.ApiException as e:
        response = json.loads(e.body)
        return "failed", response


def retrieve_transactions(client, access_token):
    try:
        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=datetime.date(2020, 1, 1),
            end_date=datetime.date(2021, 2, 1),
            options=TransactionsGetRequestOptions(),
        )
        response = client.transactions_get(request)
        transactions = response["transactions"]
        # Manipulate the count and offset parameters to paginate
        # transactions and retrieve all available data
        while len(transactions) < response["total_transactions"]:
            request = TransactionsGetRequest(
                access_token=access_token,
                start_date=datetime.date(2018, 1, 1),
                end_date=datetime.date(2018, 2, 1),
                options=TransactionsGetRequestOptions(offset=len(transactions)),
            )
        response = client.transactions_get(request)
        transactions.extend(response["transactions"])

        formatted_transaction = format_transactions(transactions)

        return "success", formatted_transaction

    except plaid.ApiException as e:
        response = json.loads(e.body)
        return "failed", response


def fire_test_event(client, access_token):
    request = ItemWebhookUpdateRequest(
        access_token=access_token,
        webhook="https://e242-2409-4042-4d9b-90e1-2537-bb1a-39ee-4436.in.ngrok.io/plaid/api/public/webhook/receive_transactions",
    )
    response = client.item_webhook_update(request)

    request = SandboxItemFireWebhookRequest(
        access_token=access_token,
        webhook_code="SYNC_UPDATES_AVAILABLE",
    )
    response = client.sandbox_item_fire_webhook(request)
    print(response)

    return "success", response.to_dict()
