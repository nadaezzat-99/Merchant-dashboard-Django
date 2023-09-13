from django.db import models
from accounts_manager.models import Account




class Terminal (models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE,db_column='user_id',related_name='user_terminal')
    vendor_name = models.CharField(max_length=100)
    terminal_type_name = models.CharField(max_length=100)
    terminal_id = models.CharField(max_length=200)
    merchant_id = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=200)
    deactivated = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    address=models.TextField(null=True,blank=True)
    date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'user: {self.user_id} - Terminal: {self.terminal_id} - merchant_id: {self.merchant_id}'

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'POS'
        verbose_name_plural = 'POS\'s'
