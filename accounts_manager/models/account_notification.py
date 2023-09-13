from django.db import models

from accounts_manager.models import Account
from notification_manager.models import Notification


class AccountNotification(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_notification')
    notification_id = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='account_notification')

    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('account_id', 'notification_id')
