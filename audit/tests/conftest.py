import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()

@pytest.fixture
def user() -> User:
    """A test user fixture"""
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    ) 