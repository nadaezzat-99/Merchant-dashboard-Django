import pytest
import requests

pytestmark = pytest.mark.django_db


class TestNotification:
    BASE_URL = 'http://127.0.0.1:8002/api/notification'

    def test_get_all_notification(self, logged_in_account, notification):
        response = logged_in_account.get('http://127.0.0.1:8000/api/notification/get_all_notifications', **logged_in_account.headers)
        content = response.json()
        assert response.status_code == 200
        assert len(content) == 1
        assert content[0]['is_read'] is False

    def test_get_all_notification_unauthorized(self, unauthorized_account, notification):
        response = unauthorized_account.get('http://127.0.0.1:8000/api/notification/get_all_notifications')
        content = response.json()
        assert response.status_code == 401
        assert content['detail'] == 'Authentication credentials were not provided.'

    def test_mark_notification_as_read_authoized(self, logged_in_account, notification):
        response = logged_in_account.get(f'http://127.0.0.1:8000/api/notification/{notification.id}/mark_as_read', **logged_in_account.headers)
        content = response.json()
        response2 = logged_in_account.get('http://127.0.0.1:8000/api/notification/get_all_notifications', **logged_in_account.headers)
        content2 = response2.json()
        assert response.status_code == 200
        assert content['message'] == 'Notification marked as read'
        assert response2.status_code == 200
        assert content2[0]['is_read'] is True

    def test_mark_notification_as_read_unauthoized(self, unauthorized_account, notification):
        response = unauthorized_account.get(f'http://127.0.0.1:8000/api/notification/{notification.id}/mark_as_read')
        content = response.json()
        assert response.status_code == 401
        assert content['detail'] == 'Authentication credentials were not provided.'
