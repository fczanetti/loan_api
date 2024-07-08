import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APIClient

from loan_api.base.models import Loan, Bank


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


@pytest.fixture
def loans(db, users):
    """
    Creates and returns 2 loans.
    """
    loans = [baker.make(Loan, client=user.username, value=250, installments=2) for user in users]
    return loans


@pytest.fixture
def loan_01(loans):
    """
    Returns loan_01.
    """
    return Loan.objects.filter(client='User Test 1').first()


@pytest.fixture
def loan_02(loans):
    """
    Returns loan_02.
    """
    return Loan.objects.filter(client='User Test 2').first()


@pytest.fixture
def bank(db):
    """
    Creates and returns a Bank instance.
    """
    return Bank.objects.create(name='Test Bank')
