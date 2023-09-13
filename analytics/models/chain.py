from django.db import models
from analytics.models import Terminal


class Chain(models.Model):
    terminal_id=models.ForeignKey(Terminal,on_delete=models.CASCADE,db_column='pos_id')
    name=models.CharField(max_length=100)
    received_id = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.terminal_id} - name= {self.name}'