import pytest
from django.contrib.auth import get_user_model
from audit.models import RequestLog
from django.contrib.auth.models import User

User = get_user_model()

@pytest.mark.django_db
class TestRequestLogModel:
    def test_request_log_creation(self) -> None:
        """Test that a RequestLog can be created"""
        log_entry = RequestLog.objects.create(
            method='GET',
            path='/test-path/',
            remote_ip='192.168.1.1',
            user=None
        )
        assert log_entry.pk is not None
        assert log_entry.method == 'GET'
        assert log_entry.path == '/test-path/'
        assert log_entry.remote_ip == '192.168.1.1'
        assert log_entry.user is None

    def test_request_log_with_user(self, user: User) -> None:
        """Test that a RequestLog can be created with a user"""
        log_entry = RequestLog.objects.create(
            method='POST',
            path='/another-path/',
            remote_ip='10.0.0.10',
            user=user
        )
        assert log_entry.pk is not None
        assert log_entry.user == user

    def test_request_log_str_representation(self) -> None:
        """Test the string representation of the RequestLog model"""
        log_entry = RequestLog.objects.create(
            method='PUT',
            path='/some/resource/',
        )
        assert str(log_entry.method) in str(log_entry)
        assert str(log_entry.path) in str(log_entry)
        assert str(log_entry.timestamp.year) in str(log_entry)
