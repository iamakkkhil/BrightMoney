from rest_framework import serializers
from plaidOauth.models import PlaidCredentials


class PlaidAccessTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaidCredentials
        fields = (
            "id",
            "item_id",
            "request_id",
            "access_token",
        )

    def create(self, validated_data):
        plaid_obj = PlaidCredentials.objects.create(
            id=validated_data["id"],
            item_id=validated_data["item_id"],
            request_id=validated_data["request_id"],
            access_token=validated_data["access_token"],
        )
        plaid_obj.save()
        return plaid_obj

    def update(self, instance, validated_data):
        instance.item_id = validated_data.get("item_id", instance.item_id)
        instance.request_id = validated_data.get("request_id", instance.request_id)
        instance.access_token = validated_data.get(
            "access_token", instance.access_token
        )
        instance.save()
        return instance
