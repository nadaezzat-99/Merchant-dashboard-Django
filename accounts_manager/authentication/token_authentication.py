from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import APIException
from django.utils import timezone
import pytz
from accounts_manager.models.token_models import Token

from merchant import settings


class InvalidToken(APIException):
    status_code = 401
    default_detail = 'Invalid Token'
    default_code = 'authentication_failed'

class UserNotActive(APIException):
    status_code = 401
    default_detail = 'User inactive or deleted'
    default_code = 'authentication_failed'

class ExpiredToken(APIException):
    status_code = 401
    default_detail = 'Token has expired'
    default_code = 'authentication_failed'

class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = Token
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise InvalidToken('Invalid token')

        if not token.user.is_active:
            raise UserNotActive('User inactive or deleted')

        # This is required for the time comparison
        utc_now = timezone.datetime.now(tz=timezone.utc)
        utc_now = utc_now.replace(tzinfo=timezone.utc)

        if token.created < utc_now - timezone.timedelta(minutes=settings.TOKEN_LIFE_TIME):
            token.delete()
            raise ExpiredToken('Token has expired')

        return token.user, token


ExpiringToken = ExpiringTokenAuthentication()