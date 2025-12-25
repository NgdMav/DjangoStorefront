import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(api_client):
    def do_auth_client(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_auth_client