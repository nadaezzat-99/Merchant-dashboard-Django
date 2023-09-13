from django.db import models


class Otp(models.Model):
    phone_number = models.CharField(max_length=100)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number

    class Meta:
        db_table = 'otp'
        verbose_name = 'Otp'
        verbose_name_plural = 'Otps'
        ordering = ['-created_at']
