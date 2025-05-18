import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from audit.middleware import RequestLogMiddleware
from audit.models import RequestLog
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest, HttpResponse

User = get_user_model()

@pytest.mark.django_db
class TestRequestLogMiddleware:
    def test_middleware_logs_request(self) -> None:
        """Test that the middleware creates a RequestLog entry"""
        factory = RequestFactory()
        request: HttpRequest = factory.get('/test-path/')
        request.user = AnonymousUser()

        def get_response(request: HttpRequest) -> None:
            return None

        middleware = RequestLogMiddleware(get_response)

        assert RequestLog.objects.count() == 0

        middleware(request)

        assert RequestLog.objects.count() == 1
        log_entry = RequestLog.objects.first()
        assert log_entry.method == 'GET'
        assert log_entry.path == '/test-path/'
        assert log_entry.remote_ip == '127.0.0.1'
        assert log_entry.user is None

    def test_middleware_logs_authenticated_user(self, user: User) -> None:
        """Test that the middleware logs the authenticated user"""
        factory = RequestFactory()
        request: HttpRequest = factory.get('/authenticated-path/')
        request.user = user

        def get_response(request: HttpRequest) -> None:
            return None

        middleware = RequestLogMiddleware(get_response)

        assert RequestLog.objects.count() == 0

        middleware(request)

        assert RequestLog.objects.count() == 1
        log_entry = RequestLog.objects.first()
        assert log_entry.user == user

    def test_middleware_handles_exception(self, monkeypatch) -> None:
        """Test that the middleware handles exceptions during log creation"""
        factory = RequestFactory()
        request: HttpRequest = factory.get('/error-path/')
        request.user = AnonymousUser()

        def mock_create(*args, **kwargs):
            raise Exception("Simulated database error")

        monkeypatch.setattr(RequestLog.objects, 'create', mock_create)

        def get_response(request: HttpRequest) -> None:
            return None

        middleware = RequestLogMiddleware(get_response)

        middleware(request)

        assert RequestLog.objects.count() == 0

    def test_middleware_processes_response(self) -> None:
        """Test that the middleware correctly calls get_response"""
        factory = RequestFactory()
        request: HttpRequest = factory.get('/response-path/')
        request.user = AnonymousUser()

        mock_response: str = "Mock Response Content"
        def get_response(request: HttpRequest) -> str:
            return mock_response

        middleware = RequestLogMiddleware(get_response)

        response = middleware(request)

        assert response == mock_response
