import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def users(db):
    """
    Creates and returns 2 users.
    """
    names = ['User Test 1', 'User Test 2']
    return [User.objects.create(username=name, password='userpass') for name in names]


@pytest.fixture
def auth_client_user_test_1(users):
    """
    Authenticate user named 'User Test 1' and
    returns an authenticated client.
    """
    user_01 = User.objects.get(username='User Test 1')
    client = APIClient()
    client.force_authenticate(user=user_01)
    return client
