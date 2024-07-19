import pytest
from rest_framework.test import APIClient
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from loan_api.base.models import Loan


@pytest.fixture
def resp_loan_removal_authenticated_user_test_1(auth_client_user_test_1, loan_01):
    """
    Creates a request removing a loan and
    returns a response.
    """
    resp = auth_client_user_test_1.delete(f'/api/loans/{loan_01.pk}/')
    return resp


def test_loan_removal(resp_loan_removal_authenticated_user_test_1):
    """
    Certifies that the response has a 204 status code and
    the loan was deleted.
    """
    assert resp_loan_removal_authenticated_user_test_1.status_code == HTTP_204_NO_CONTENT
    assert not Loan.objects.filter(client__email='user_01@email.com').exists()


def test_user_can_not_remove_loan_from_others(auth_client_user_test_1, loan_02):
    """
    Certifies that a user can not remove
    loans that belong to others.
    """
    resp = auth_client_user_test_1.delete(f'/api/loans/{loan_02.pk}/')
    assert resp.status_code == HTTP_404_NOT_FOUND


def test_unauthenticated_users_can_not_remove_loans(loan_01):
    """
    Certifies a non authenticated user can not
    remove a loan.
    """
    client = APIClient()
    resp = client.delete(f'/api/loans/{loan_01.pk}/')
    assert resp.status_code == HTTP_401_UNAUTHORIZED
