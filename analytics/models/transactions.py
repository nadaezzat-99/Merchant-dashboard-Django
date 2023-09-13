from django.db import models
from django.db.models import signals
from django.dispatch import receiver

from accounts_manager.models.accounts import Account
from analytics.models import Terminal



pos_types = (
    ('sale', 'Sale'),
    ('refund', 'Refund')
)

connection_types=(
    ('online','Online'),
    ('offline','Offline')
)


class Transactions(models.Model):
    terminal_id = models.ForeignKey(Terminal, on_delete=models.CASCADE,db_column='terminal_id')
    aman_batch_id = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=pos_types, default='sale')
    # TODO: remove null and blank fields
    date = models.DateTimeField(null=True, blank=True)
    header1 = models.CharField(max_length=100)
    header2 = models.CharField(max_length=100)
    header3 = models.CharField(max_length=100)
    mapping_type = models.CharField(max_length=100, null=True, blank=True)
    mapping_status = models.CharField(max_length=100, null=True, blank=True)
    batch_id = models.CharField(max_length=100)
    stan = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    is_settled = models.BooleanField(default=False)
    settlement_reference = models.CharField(max_length=100,null=True, blank=True)
    settlement_date = models.DateTimeField(null=True, blank=True)
    rrn = models.CharField(max_length=100)
    mdr = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    entry_mode = models.CharField(max_length=100)
    connection_on_off = models.CharField(max_length=50,choices=connection_types,default='online')
    emv_trx = models.BooleanField(default=False)
    dcc_trx = models.BooleanField(default=False)
    is_installment = models.BooleanField(default=False)
    is_void = models.BooleanField(default=False)
    response_code = models.CharField(max_length=100)
    response_message = models.CharField(max_length=100)
    auth_id= models.CharField(max_length=100)

    
    def __str__(self):
        return f'{self.terminal_id} - {self.stan} - {self.date}'

    class Meta:
        ordering = ['-date']
        verbose_name = 'POS Data'
        verbose_name_plural = 'POS Data'

# signal
@receiver(signals.pre_save, sender=Transactions)
def transaction_save(sender, instance, **kwargs):
    if instance.type == 'sale':
        if not instance.is_void and not instance.is_installment:
            instance.mapping_type = 'sale'
        elif  instance.is_void and instance.is_installment:
            instance.mapping_type = 'void installment'
        elif  instance.is_void:
            instance.mapping_type = 'void sale'
        elif  instance.is_installment:
            instance.mapping_type = 'installment'
    else:
        instance.mapping_type = 'refund'

    if instance.is_settled:
        instance.mapping_status = 'Settled'
    else:
        instance.mapping_status = instance.response_message

    




