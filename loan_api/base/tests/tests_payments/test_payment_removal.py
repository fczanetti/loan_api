import pytest
from rest_framework.test import APIClient
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from loan_api.base.models import Payment


@pytest.fixture
def resp_payment_removal_authenticated_user_test_1(auth_client_user_test_1, payment_loan_01):
    """
    Creates a request removing a payment and
    returns a response.
    """
    resp = auth_client_user_test_1.delete(f'/api/payments/{payment_loan_01.pk}/')
    return resp


def test_payment_removal(resp_payment_removal_authenticated_user_test_1, loan_01):
    """
    Certifies that the response has a 204 status code and
    the payment was deleted.
    """
    assert resp_payment_removal_authenticated_user_test_1.status_code == HTTP_204_NO_CONTENT
    assert not Payment.objects.filter(loan=loan_01).exists()


def test_user_can_not_remove_payment_from_others(auth_client_user_test_1, payment_loan_02):
    """
    Certifies that a user can not remove
    payments that belong to others.
    """
    resp = auth_client_user_test_1.delete(f'/api/payments/{payment_loan_02.pk}/')
    assert resp.status_code == HTTP_404_NOT_FOUND


def test_unauthenticated_users_can_not_remove_payments(payment_loan_01):
    """
    Certifies a non authenticated user can not
    remove a payment.
    """
    client = APIClient()
    resp = client.delete(f'/api/payments/{payment_loan_01.pk}/')
    assert resp.status_code == HTTP_401_UNAUTHORIZED
