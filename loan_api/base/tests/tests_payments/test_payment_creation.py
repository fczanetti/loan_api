import pytest

from loan_api.base.models import Loan, Payment
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient
from loan_api.base.serializers import PaymentSerializer


@pytest.fixture
def resp_payment_creation_authenticated_user_test_1(auth_client_user_test_1, loan_01):
    """
    Makes a POST request to create a payment
    and returns a response.
    """
    data = {'loan': loan_01.pk, 'value': 100}
    resp = auth_client_user_test_1.post('/api/payments/', data=data)
    return resp


def test_resp_payment_creation_status_code(resp_payment_creation_authenticated_user_test_1):
    """
    Certifies the request was successfull and returned
    a response with a 201 status code.
    """
    assert resp_payment_creation_authenticated_user_test_1.status_code == HTTP_201_CREATED


def test_payment_created_present_in_response(resp_payment_creation_authenticated_user_test_1, loan_01):
    """
    Certifies that the payment created is returned in the response.
    """
    payment = Payment.objects.filter(loan=loan_01).first()
    serializer = PaymentSerializer(payment)
    assert resp_payment_creation_authenticated_user_test_1.json() == serializer.data


def test_user_1_can_not_create_payments_for_user_2(auth_client_user_test_1, loan_02):
    """
    Certifies a user can not create payments for
    loans that belong to other users.
    """
    data = {'loan': loan_02.pk, 'value': 25}
    resp = auth_client_user_test_1.post('/api/payments/', data=data)
    assert resp.status_code == HTTP_400_BAD_REQUEST


def test_unauthenticated_users_can_not_create_payments(loans):
    """
    Certifies that non authenticated users are not
    able to create payments.
    """
    loan = Loan.objects.first()
    data = {'loan': loan.pk, 'value': 25}
    client = APIClient()
    resp = client.post('/api/payments/', data=data)
    assert resp.status_code == HTTP_401_UNAUTHORIZED


def test_invalid_input(auth_client_user_test_1, loan_01):
    """
    Certifies invalid inputs return a
    bad request (400) response.
    """
    data_01 = {'loan': 5, 'value': 100}           # Invalid loan ID;
    data_02 = {'loan': '', 'value': 100}          # Invalid loan ID;
    data_03 = {'loan': loan_01.pk, 'value': 'a'}  # Invalid value;
    data_04 = {}                                  # Invalid data;

    resp_01 = auth_client_user_test_1.post('/api/payments/', data=data_01)
    resp_02 = auth_client_user_test_1.post('/api/payments/', data=data_02)
    resp_03 = auth_client_user_test_1.post('/api/payments/', data=data_03)
    resp_04 = auth_client_user_test_1.post('/api/payments/', data=data_04)

    assert resp_01.status_code == HTTP_400_BAD_REQUEST
    assert resp_02.status_code == HTTP_400_BAD_REQUEST
    assert resp_03.status_code == HTTP_400_BAD_REQUEST
    assert resp_04.status_code == HTTP_400_BAD_REQUEST
