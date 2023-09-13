from django.db import models
from accounts_manager.models import Account


class BankDetails(models.Model):
    user_id=models.ForeignKey(Account,on_delete=models.CASCADE,db_column='user_id')
    bank_name=models.CharField(max_length=100)
    bank_branch=models.CharField(max_length=100)
    account_number=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.user_id} - account number: {self.account_number}'