from rest_framework import serializers

from analytics.models import Acquire


class AcquireSerializer(serializers.ModelSerializer):

    class Meta:
        model = Acquire
        fields = ['received_id','name','terminal_id']

