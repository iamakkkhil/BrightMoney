from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.authtoken.models import Token


class TokenPairSerializer(TokenObtainPairSerializer):
    """
    Serializer for TokenObtainPair.

    This is used to get the token pair for the user.
    """

    @classmethod
    def get_token(cls, user):
        """
        Override get_token method to add custom claims.

        :param user: User object
        :return: Token object
        """
        token = super().get_token(user)
        token["name"] = user.get_full_name

        return token


def get_tokens_for_user(user):
    """
    Get a token pair for a user.

    Parameters
    ----------
    user: User object.
    device: TOTP device object.

    Returns
    -------
    Dictionary of (refresh token, access token).

    """
    serializer = TokenPairSerializer()
    refresh = serializer.get_token(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
