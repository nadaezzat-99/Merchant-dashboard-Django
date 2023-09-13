import pytest
import requests
from pytest_django.lazy_django import skip_if_no_django
from rest_framework.test import APIClient

from accounts_manager.factories.account_factory import AccountFactory
from accounts_manager.models import Account
from notification_manager.factories.notification_factory import NotificationFactory

LOGIN_URL = '/api/auth/login'


@pytest.fixture
def account() -> Account:
    account = AccountFactory()
    account.set_password('123456')
    account.save()
    return account


@pytest.fixture
def logged_in_account(account: Account) -> APIClient:
    client = APIClient()
    base_url = 'http://127.0.0.1:8000/api/auth/login'
    data = {
        "phone_number": account.username,
        "password": "123456"
    }
    response = client.post(base_url, data=data)
    content = response.json()
    token = content['data']['token']
    client.headers = {
        'HTTP_AUTHORIZATION': 'Token ' + token,
    }
    return client


@pytest.fixture
def unauthorized_account(account: Account) -> APIClient:
    client = APIClient()
    return client


@pytest.fixture
def notification():
    notification = NotificationFactory()
    return notification
