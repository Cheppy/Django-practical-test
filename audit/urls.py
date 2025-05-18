from django.urls import path
from . import views

urlpatterns = [
    path('', views.request_log_list, name='request_log_list'),
] 