import datetime

from django.contrib import admin
from django.utils.timezone import utc

from notification_manager.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    def is_archived(self, obj):
        if obj.created_at.replace(tzinfo=None) < (datetime.datetime.now() - datetime.timedelta(days=14)).replace(tzinfo=None):
            return True
        else:
            return False

    list_display = ('id', 'title', 'description', 'created_at', 'is_archived', )


admin.site.register(Notification, NotificationAdmin)
