import factory
from factory.django import DjangoModelFactory

from accounts_manager.models import Account


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    # phone_number = '01097654964'
    username = factory.Faker('phone_number')
    name = factory.Faker('name')
    email = factory.Faker('email')
