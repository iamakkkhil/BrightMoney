import plaid
import os
from plaid.api import plaid_api
from dotenv import load_dotenv

load_dotenv()


configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        "clientId": os.getenv("plaidClientId"),
        "secret": os.getenv("plaidSecret"),
    },
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)
