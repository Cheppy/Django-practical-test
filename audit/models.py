from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    remote_ip = models.GenericIPAddressField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.timestamp} - {self.method} {self.path}"

    class Meta:
        ordering = ['timestamp']
