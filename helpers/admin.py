from django.contrib import admin
from django.contrib.admin import ModelAdmin

from helpers.models import GeneralInfo


# Register your models here.

# Apply summernote to all TextField in model.
class GeneralInfoAdmin(ModelAdmin):
    # summernote_fields = ('terms_and_conditions', 'privacy_and_policy')
    list_display = ('id', 'terms_and_conditions', 'terms_and_conditions_ar', 'privacy_and_policy', 'privacy_and_policy_ar', 'whatsapp_number', 'facebook_link', 'twitter_link')

admin.site.register(GeneralInfo, GeneralInfoAdmin)
