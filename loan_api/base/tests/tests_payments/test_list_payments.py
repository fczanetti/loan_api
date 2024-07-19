from datetime import date

import pytest
from model_bakery import baker

from loan_api.base.models import Payment, Loan
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient
from loan_api.base.serializers import PaymentSerializer


@pytest.fixture
def payments(db, loans):
    """
    Creates and returns two payments.
    """
    payments = [baker.make(Payment, loan=loan, value=30, payment_date=date.today()) for loan in loans]
    return payments


@pytest.fixture
def resp_list_payments_authenticated_user_test_1(auth_client_user_test_1, payments):
    """
    Creates a request to list the payments from user
    named 'User Test 1' and returns the response.
    """
    resp = auth_client_user_test_1.get('/api/payments/')
    return resp


def test_status_code_list_payments(resp_list_payments_authenticated_user_test_1):
    """
    Certifies the response returned with
    a 200 status code.
    """
    assert resp_list_payments_authenticated_user_test_1.status_code == HTTP_200_OK


def test_payments_from_other_users_not_present(resp_list_payments_authenticated_user_test_1, payments):
    """
    Certifies that only payments from the requesting user are present.
    """
    payment_01 = Payment.objects.filter(loan__client='user_01@email.com').first()
    payment_02 = Payment.objects.filter(loan__client='user_02@email.com').first()
    serializer_01 = PaymentSerializer(payment_01)
    serializer_02 = PaymentSerializer(payment_02)
    assert serializer_01.data in resp_list_payments_authenticated_user_test_1.json()['results']
    assert serializer_02.data not in resp_list_payments_authenticated_user_test_1.json()['results']


def test_unauthenticated_request_not_authorized(db):
    """
    Certifies that a non authenticated user can
    not make requests to see payments.
    """
    client = APIClient()
    resp = client.get('/api/payments/')
    assert resp.status_code == HTTP_401_UNAUTHORIZED


def test_filter_payments_by_loan_id(auth_client_user_test_1, loan_01):
    """
    Certifies payments can be filtered by loan id.
    """
    new_loan = baker.make(Loan, client='user_01@email.com', request_date=date.today())

    payment_1 = Payment.objects.create(loan=loan_01, value=25, payment_date=date.today())
    new_payment = Payment.objects.create(loan=new_loan, value=35, payment_date=date.today())

    serializer_1 = PaymentSerializer(payment_1)
    serializer_new_payment = PaymentSerializer(new_payment)

    resp = auth_client_user_test_1.get(f'/api/payments/?loan={loan_01.pk}')

    assert serializer_1.data in resp.json()['results']
    assert serializer_new_payment.data not in resp.json()['results']
