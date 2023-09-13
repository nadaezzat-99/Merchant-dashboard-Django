import factory

from accounts_manager.factories.account_factory import AccountFactory
from notification_manager.models import Notification


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    title = factory.Faker('sentence', nb_words=6, variable_nb_words=True)
    description = factory.Faker('text', max_nb_chars=200)
    created_by = factory.SubFactory(AccountFactory)
    updated_by = factory.SubFactory(AccountFactory)
