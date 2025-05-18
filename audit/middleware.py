from .models import RequestLog
from django.http import HttpRequest, HttpResponse

class RequestLogMiddleware:
    def __init__(self, get_response: callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        try:
            request_log = RequestLog.objects.create(
                method=request.method,
                path=request.path,
                remote_ip=request.META.get('REMOTE_ADDR'),
                user=request.user if request.user.is_authenticated else None
            )
        except Exception:
            import logging
            logger = logging.getLogger(__name__)
            logger.error("Error saving request log", exc_info=True)

        response = self.get_response(request)


        return response 