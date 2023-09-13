from django.utils import timezone

from accounts_manager.authentication.token_authentication import Token
from accounts_manager.models import Account
from rest_framework import serializers

from analytics.models import Terminal
from analytics.serializers import TerminalSerializer
from merchant import settings


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        if 'fields' in self.context:
            fields = self.context['fields']
            if fields:
                # Drop any fields that are not specified in the `fields` argument.
                allowed = set(fields)
                existing = set(self.fields.keys())
                for field_name in existing - allowed:
                    self.fields.pop(field_name)

class AccountSerializer(DynamicFieldsModelSerializer):
    token = serializers.SerializerMethodField()
    token_life_time = serializers.SerializerMethodField()
    pos = serializers.SerializerMethodField()

    def get_token(self, obj):
        token = Token.objects.create(user=obj)
        return str(token)

    def get_token_life_time(self, obj):
        return settings.TOKEN_LIFE_TIME


    def get_pos(self, obj):
        POSs = Terminal.objects.filter(user_id=obj, deactivated=False)
        serializer = TerminalSerializer(POSs, many=True)
        return serializer.data


    class Meta:
        model = Account
        exclude = ['force_password_change_on_first_time', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'groups', 'user_permissions']
        read_only_fields = ['created_at', 'updated_at', 'token', 'password']
        extra_fields = ['pos']


class AccountCreateUpdateSerializer(serializers.ModelSerializer):
    pos = serializers.SerializerMethodField()

    def get_pos(self, obj):
        POSs = Terminal.objects.filter(user_id=obj)
        serializer = TerminalSerializer(POSs, many=True)
        return serializer.data

    class Meta:
        model = Account
        fields=['id','name','username','email','date', 'pos']

