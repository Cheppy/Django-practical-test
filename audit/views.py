from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import RequestLog


def request_log_list(request: HttpRequest) -> HttpResponse:
    """Display the 10 most recent request logs."""
    latest_logs = RequestLog.objects.order_by('-timestamp')[:10]
    context = {
        'latest_logs': latest_logs
    }
    return render(request, 'audit/request_log_list.html', context)
