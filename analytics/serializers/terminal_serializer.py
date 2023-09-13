from rest_framework import serializers

from analytics.models import Terminal


class TerminalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Terminal
        fields = '__all__'

