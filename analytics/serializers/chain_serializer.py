from rest_framework import serializers

from analytics.models import Chain


class ChainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chain
        fields = ['received_id','name','terminal_id']

