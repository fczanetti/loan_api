import pytest

from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient
from loan_api.base.serializers import PaymentSerializer


@pytest.fixture
def resp_retrieve_payment_authenticated_user_test_1(auth_client_user_test_1, payment_loan_01):
    """
    Creates a request retrieving a payment and returns a response.
    """
    resp = auth_client_user_test_1.get(f'/api/payments/{payment_loan_01.pk}/')
    return resp


def test_status_code_retrieve_payment(resp_retrieve_payment_authenticated_user_test_1):
    """
    Certifies that the response is successfull with a 200 status code.
    """
    assert resp_retrieve_payment_authenticated_user_test_1.status_code == HTTP_200_OK


def test_payment_present_in_response(resp_retrieve_payment_authenticated_user_test_1, payment_loan_01):
    """
    Certifies that:
    - the payment is present in the response;
    - all necessary fields are shown;
    - value is returned as a float instance.
    """
    serializer = PaymentSerializer(payment_loan_01)
    payment_data = {'id': serializer.data['id'],
                    'loan': serializer.data['loan'],
                    'payment_date': serializer.data['payment_date'],
                    'value': serializer.data['value']}
    assert resp_retrieve_payment_authenticated_user_test_1.json() == payment_data
    assert isinstance(serializer.data['value'], float)


def test_user_1_can_not_retrieve_payments_from_user_2(loan_02, auth_client_user_test_1, payment_loan_02):
    """
    Certifies that a user can not retrieve payments from others.
    """
    resp = auth_client_user_test_1.get(f'/api/payments/{payment_loan_02.pk}/')
    assert resp.status_code == HTTP_404_NOT_FOUND


def test_unauthenticated_users_can_not_retrieve_payments(payment_loan_01):
    """
    Certifies that a non authenticated user can not retrieve payments.
    """
    client = APIClient()
    resp = client.get(f'/api/payments/{payment_loan_01.pk}/')
    assert resp.status_code == HTTP_401_UNAUTHORIZED
