from django.db import models


class GeneralInfo(models.Model):

    terms_and_conditions = models.TextField(null=True, blank=True)
    terms_and_conditions_ar = models.TextField(null=True, blank=True)

    privacy_and_policy = models.TextField(null=True, blank=True)
    privacy_and_policy_ar = models.TextField(null=True, blank=True)

    whatsapp_number = models.CharField(max_length=255, null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)


