from rest_framework import serializers

from accounts_manager.serializers.account_serializer import DynamicFieldsModelSerializer
from notification_manager.models import Notification


class NotificationSerializer(DynamicFieldsModelSerializer):
    is_read = serializers.SerializerMethodField()
    title_lang = serializers.SerializerMethodField()
    description_lang = serializers.SerializerMethodField()

    def get_is_read(self, obj):
        if 'request' in self.context:
            account = self.context['request'].user
            if account.account_notification.filter(notification_id=obj).exists():
                return account.account_notification.get(notification_id=obj).is_read
        return False

    def get_title_lang(self, obj):
        if 'request' in self.context:
            lang = self.context['request'].headers.get('Accept-Language', 'en')
            if lang == 'ar':
                return obj.title_ar
        return obj.title


    def get_description_lang(self, obj):
        if 'request' in self.context:
            lang = self.context.get('request').headers.get('Accept-Language', 'en')
            if lang == 'ar':
                return obj.description_ar
        return obj.description

    class Meta:
        model = Notification
        fields = '__all__'
