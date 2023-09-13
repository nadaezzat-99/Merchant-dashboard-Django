import datetime

import requests
from rest_framework import permissions

from merchant import settings


class IsVendor(permissions.BasePermission):
    """
    Allows access only to authenticated super admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.type == 'vendor')


class IsMerchant(permissions.BasePermission):
    """
    Allows access only to authenticated super admin users.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.type == 'merchant':
            print((request.user.auth_token.created + datetime.timedelta(minutes=30)).timestamp() , datetime.datetime.now().timestamp())
            if (request.user.auth_token.created + datetime.timedelta(minutes=30)).timestamp() < datetime.datetime.now().timestamp():
                return False
            phone_number = request.user.username
            response = requests.get(f'{settings.AMAN_API_URL}merchant/check?phone={phone_number}', verify=False)
            content = response.json()
            if not content['responseCode'] == 200:
                return False
            if not content['responseData']['hasPOSs']:
                request.user.auth_token.delete()
                request.user.has_pos = False
                request.user.save()
                return False
            return True
        return False
