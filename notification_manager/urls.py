from django.urls import path

from notification_manager.views.notification_views import NotificationViews

app_name = "notification_manager"
urlpatterns = [
    path('get_all_notifications', NotificationViews.as_view({'get': 'list'}), name='get_all_notifications'),
    path('<int:pk>/mark_as_read', NotificationViews.as_view({'get': 'mark_as_read'}), name='mark_as_read'),

]
