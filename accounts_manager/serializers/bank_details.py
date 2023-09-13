from rest_framework import serializers

from accounts_manager.models import BankDetails


class BankDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankDetails
        fields = ['user_id','bank_name','bank_branch','account_number']

