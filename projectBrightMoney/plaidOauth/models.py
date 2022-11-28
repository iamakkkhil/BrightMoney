import uuid
from django.db import models
from accounts.models import User

# Create your models here.
class PlaidCredentials(models.Model):
    id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    item_id = models.CharField(max_length=100)
    request_id = models.CharField(max_length=100)
    access_token = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Account(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=100)
    balances = models.JSONField(null=True)
    mask = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    official_name = models.CharField(max_length=100, null=True)
    subtype = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.CharField(max_length=100)
    institution_id = models.CharField(max_length=100, null=True)
    webhook = models.CharField(max_length=100, null=True)
    error = models.JSONField(null=True)
    available_products = models.JSONField(null=True)
    billed_products = models.JSONField(null=True)
    products = models.JSONField(null=True)
    consented_products = models.JSONField(null=True)
    consent_expiration_time = models.DateTimeField(null=True)
    update_type = models.CharField(max_length=100)

    def __str__(self):
        return self.item_id
