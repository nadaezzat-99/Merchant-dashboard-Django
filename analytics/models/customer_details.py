from django.db import models
from analytics.models import Transactions


class CustomerDetails(models.Model):
    transaction_id = models.ForeignKey(
        Transactions, on_delete=models.CASCADE, db_column='transaction_id')
    issuer = models.CharField(max_length=100)
    pan = models.CharField(max_length=100)
    card_holder_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.transaction_id} - customer name: {self.card_holder_name}'
