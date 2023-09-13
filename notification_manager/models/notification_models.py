from django.db import models
from accounts_manager.models import Account


# Create your models here.

class Notification(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    title_ar = models.CharField(max_length=255, null=True, blank=True)

    description = models.TextField(null=True, blank=True)
    description_ar = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.title}'
