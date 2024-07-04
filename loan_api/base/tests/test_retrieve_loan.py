import pytest

from loan_api.base.models import Loan, Payment
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient
from model_bakery import baker


@pytest.fixture
def resp_retrieve_loan_authenticated_user_test_1(auth_client_user_test_1, loans):
    """
    Creates a request to retrieve a loan that
    belongs to 'User Test 1' and returns a response.
    """
    loan = Loan.objects.filter(client='User Test 1').first()
    baker.make(Payment, loan=loan, value=50)
    baker.make(Payment, loan=loan, value=60)
    resp = auth_client_user_test_1.get(f'/api/loans/{loan.pk}/')
    return resp


def test_status_code_retrieve_loan(resp_retrieve_loan_authenticated_user_test_1):
    """
    Certifies the response is successfull with
    a 200 status code.
    """
    assert resp_retrieve_loan_authenticated_user_test_1.status_code == HTTP_200_OK


def test_retrieve_loan_from_other_client_not_found(auth_client_user_test_1, loans):
    """
    Certifies that a user can not retrieve
    loans from others.
    """
    loan_user_2 = Loan.objects.filter(client='User Test 2').first()
    resp = auth_client_user_test_1.get(f'/api/loans/{loan_user_2.pk}/')
    assert resp.status_code == HTTP_404_NOT_FOUND


def test_payments_present_in_resp_content(resp_retrieve_loan_authenticated_user_test_1):
    """
    Certifies that the payments related to the
    Loan retrieved are listed in the response.
    """
    resp_json = resp_retrieve_loan_authenticated_user_test_1.json()
    loan_id = resp_json['id']

    # List of payments related to the retrieved Loan
    payment_set = resp_json.get('payment_set')

    # Loan retrieved
    loan = Loan.objects.get(id=loan_id)

    # Certifying that there is a field to list payments
    assert payment_set is not None

    # Certifying the payments created are listed in payment_set
    for i, payment in enumerate(loan.payment_set.all()):
        assert str(payment.pk) in payment_set[i]


def test_unauthenticated_user_can_not_retrieve_loans():
    """
    Certifies that non authenticated users can not
    retrieve loans.
    """
    client = APIClient()
    resp = client.get('/api/loans/')
    assert resp.status_code == HTTP_401_UNAUTHORIZED
