from rest_framework import serializers

from analytics.models import CustomerDetails


class CustomerDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerDetails
        fields = ['transaction_id','issuer','pan','card_holder_name']
