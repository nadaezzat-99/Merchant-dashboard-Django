import datetime

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts_manager.models import AccountNotification
from accounts_manager.permissions import IsMerchant
from notification_manager.models import Notification
from notification_manager.serializers.notification_serializers import NotificationSerializer


class NotificationViews(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Notification.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        two_weeks_ago = datetime.datetime.now() - datetime.timedelta(days=14)
        queryset = self.get_queryset()
        account_notification = []
        if 'unread' in request.GET and bool(request.GET.get('unread', 'false') == 'true'):
            account_notification = request.user.account_notification.all().values_list('notification_id', flat=True)
        queryset = queryset.filter(created_at__gte=two_weeks_ago).exclude(pk__in=account_notification)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # print(self.get_paginated_response(serializer.data).__dict__)
            res = self.get_paginated_response(serializer.data).data
            if 'unread' in request.GET and bool(request.GET.get('unread', 'false') == 'true'):
                res['num_of_unread'] = queryset.count()
            else:
                res['num_of_unread'] = queryset.count() - request.user.account_notification.count()
            return Response(data=res, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def mark_as_read(self, request, *args, **kwargs):
        account = request.user
        notification = self.get_object()
        account_notification, created = AccountNotification.objects.get_or_create(account_id=account, notification_id=notification)
        account_notification.is_read = True
        account_notification.save()
        return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)


