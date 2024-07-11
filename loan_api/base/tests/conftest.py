import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from loan_api.base.models import Loan, Bank, Payment, User


@pytest.fixture
def users(db):
    """
    Creates and returns 2 users.
    """
    names = ['user_01@email.com', 'user_02@email.com']
    return [User.objects.create(email=name, password='userpass') for name in names]


@pytest.fixture
def auth_client_user_test_1(users):
    """
    Authenticate user user_01@email.com and
    returns an authenticated client.
    """
    user_01 = User.objects.get(email='user_01@email.com')
    client = APIClient()
    client.force_authenticate(user=user_01)
    return client


@pytest.fixture
def loans(db, users):
    """
    Creates and returns 2 loans.
    """
    loans = [baker.make(Loan, client=user.email, value=250, installments=2) for user in users]
    return loans


@pytest.fixture
def loan_01(loans):
    """
    Returns loan_01.
    """
    return Loan.objects.filter(client='user_01@email.com').first()


@pytest.fixture
def loan_02(loans):
    """
    Returns loan_02.
    """
    return Loan.objects.filter(client='user_02@email.com').first()


@pytest.fixture
def bank(db):
    """
    Creates and returns a Bank instance.
    """
    return Bank.objects.create(name='Test Bank')


@pytest.fixture
def payment_loan_01(db, loan_01):
    """
    Creates and returns a payment.
    """
    payment = Payment.objects.create(loan=loan_01, value=20)
    return payment


@pytest.fixture
def payment_loan_02(db, loan_02):
    """
    Creates and returns a payment.
    """
    payment = Payment.objects.create(loan=loan_02, value=20)
    return payment
