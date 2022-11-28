from django.contrib import admin
from plaidOauth.models import PlaidCredentials, Account, Item

# Register your models here.
admin.site.register(PlaidCredentials)
admin.site.register(Account)
admin.site.register(Item)
