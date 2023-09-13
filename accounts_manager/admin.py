from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import TokenProxy
from accounts_manager.models.otp import Otp
from accounts_manager.models.token_models import Token
from accounts_manager.models import Account, Otp, BankDetails, AccountNotification

class OtpTokenAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'otp', 'created_at', 'verified')

admin.site.register(Account)
admin.site.register(Otp, OtpTokenAdmin)
admin.site.unregister(Group)

admin.site.unregister(TokenProxy)

# admin.site.register(Otp)

# admin.site.register(BankDetails)
# admin.site.register(AccountNotification)

