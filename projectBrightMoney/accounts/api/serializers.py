from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from accounts.models import User
from utils.serializers import get_tokens_for_user


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                "User with given email and password does not exists."
            )
        try:
            tokens = get_tokens_for_user(user)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with given email and password does not exists"
            )
        return {
            "email": user.email,
            "tokens": tokens,
        }


class UserSignupSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "is_active",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        """
        Create a new user
        :param validated_data:
        :return:
        """
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update an existing user
        :param instance:
        :param validated_data:
        :return:
        """
        instance.email = validated_data.get("email", instance.email)
        instance.mobile_number = validated_data.get(
            "mobile_number", instance.mobile_number
        )
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.set_password(validated_data.get("password", instance.password))
        instance.save()
        update_last_login(None, instance)
        return instance
