import pytest
from django.urls import reverse
from django.test import Client
from audit.models import RequestLog
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from typing import Callable

User = get_user_model()

@pytest.fixture
def client() -> Client:
    return Client()

@pytest.fixture
def create_request_logs() -> Callable[[int], list[RequestLog]]:
    def _create_request_logs(count: int) -> list[RequestLog]:
        logs = []
        for i in range(count):
            timestamp = datetime.now() - timedelta(seconds=i)
            log_entry = RequestLog.objects.create(
                method='GET',
                path=f'/fake-path-{i}/',
                timestamp=timestamp
            )
            logs.append(log_entry)
        return sorted(logs, key=lambda x: x.timestamp, reverse=True)
    return _create_request_logs

@pytest.mark.django_db
class TestRequestLogView:
    def test_request_log_list_view(self, client: Client, create_request_logs: Callable[[int], list[RequestLog]]) -> None:
        """Test the request_log_list view displays the latest 10 logs"""
        created_logs = create_request_logs(15)

        url = reverse('request_log_list')
        response = client.get(url)

        assert response.status_code == 200
        assert 'audit/request_log_list.html' in [t.name for t in response.templates]

        latest_logs_in_context = response.context['latest_logs']

        assert len(latest_logs_in_context) == 10

        all_logs_in_db = RequestLog.objects.order_by('-timestamp')
        expected_latest_logs = list(all_logs_in_db[:10])

        assert list(latest_logs_in_context) == expected_latest_logs

    def test_request_log_list_view_empty(self, client: Client) -> None:
        """Test the request_log_list view with no log entries initially"""
        url = reverse('request_log_list')
        response = client.get(url)

        assert response.status_code == 200
        assert 'audit/request_log_list.html' in [t.name for t in response.templates]

        latest_logs_in_context = response.context['latest_logs']

        assert len(latest_logs_in_context) == 1
        log_entry = latest_logs_in_context[0]
        assert log_entry.method == 'GET'
        assert log_entry.path == '/logs/'
