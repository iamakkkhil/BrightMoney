from rest_framework_simplejwt.tokens import RefreshToken
from utils.plaidUtils import retrieve_accounts
from plaidOauth.models import Account, Item
from utils.plaidApiClient import client
from accounts.models import User
from celery import shared_task


def blacklist_tokens(usertoken):
    """
    Logout a user.

    Parameters
    ----------
    usertoken: UserToken object.

    Returns
    -------
    Boolean (True or False) depending upon the successful logout.
    """
    try:
        token = RefreshToken(usertoken)
        token.blacklist()
        return True
    except Exception as e:
        print(e)
        return False


@shared_task(name="fetching_account_data_from_plaid")
def saved_retrieved_accounts_db(access_token, user_id):
    """
    Retrieve all the accounts from plaid and save into the database.
    """
    user = User.objects.get(pk=user_id)

    _status, data = retrieve_accounts(client, access_token)
    if _status != "success":
        return _status

    accounts = data.get("accounts", [])
    item = data.get("item", {})

    try:
        for account in accounts:
            account_obj = Account.objects.create(
                user_id=user,
                account_id=account.get("account_id", None),
                balances=account.get("balances", None),
                mask=account.get("mask", None),
                name=account.get("name", None),
                official_name=account.get("official_name", None),
                subtype=account.get("subtype", None),
                type=account.get("type", None),
            )
            account_obj.save()

        item_obj = Item.objects.create(
            user_id=user,
            item_id=item.get("item_id", None),
            institution_id=item.get("institution_id", None),
            webhook=item.get("webhook", None),
            error=item.get("error", None),
            available_products=item.get("available_products", None),
            billed_products=item.get("billed_products", None),
            products=item.get("products", None),
            consented_products=item.get("consented_products", None),
            consent_expiration_time=item.get("consent_expiration_time", None),
            update_type=item.get("update_type", None),
        )
        item_obj.save()
        return "success"

    except Exception as e:
        print(e)
        return "failed"


def get_saved_accounts(user):
    accounts = Account.objects.filter(user_id=user)
    account_list = list()
    for account in accounts:
        account_list.append(
            {
                "account_id": account.account_id,
                "balances": account.balances,
                "mask": account.mask,
                "name": account.name,
                "official_name": account.official_name,
                "subtype": account.subtype,
                "type": account.type,
            }
        )

    return account_list
