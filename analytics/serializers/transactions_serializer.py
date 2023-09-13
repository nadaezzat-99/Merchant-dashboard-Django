from rest_framework import serializers

from analytics.models import  Transactions




class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'
        # read_only_fields = ('id', 'created_at', 'updated_at')