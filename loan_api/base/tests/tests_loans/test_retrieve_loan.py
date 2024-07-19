from datetime import date

import pytest

from loan_api.base.models import Payment
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient
from model_bakery import baker

from loan_api.base.serializers import LoanSerializer


@pytest.fixture
def resp_retrieve_loan_authenticated_user_test_1(auth_client_user_test_1, loan_01):
    """
    Creates a request to retrieve a loan that
    belongs to 'User Test 1' and returns a response.
    """
    baker.make(Payment, loan=loan_01, value=50, payment_date=date.today())
    baker.make(Payment, loan=loan_01, value=60, payment_date=date.today())
    resp = auth_client_user_test_1.get(f'/api/loans/{loan_01.pk}/')
    return resp


def test_status_code_retrieve_loan(resp_retrieve_loan_authenticated_user_test_1):
    """
    Certifies the response is successfull with
    a 200 status code.
    """
    assert resp_retrieve_loan_authenticated_user_test_1.status_code == HTTP_200_OK


def test_loan_format_in_response(resp_retrieve_loan_authenticated_user_test_1, loan_01):
    """
    Certifies that:
    - the loan is present in the response and all necessary infos are shown;
    - sum of payments is correct;
    - the value is returned as a float instance;
    """
    serializer = LoanSerializer(loan_01)
    loan_data = {'id': serializer.data['id'],
                 'value': serializer.data['value'],
                 'interest_rate': serializer.data['interest_rate'],
                 'installments': serializer.data['installments'],
                 'installment_value': serializer.data['installment_value'],
                 'ip_address': serializer.data['ip_address'],
                 'request_date': serializer.data['request_date'],
                 'bank': serializer.data['bank'],
                 'client': serializer.data['client'],
                 'payment_sum':  serializer.data['payment_sum'],
                 'unpaid_value': serializer.data['unpaid_value']}
    assert resp_retrieve_loan_authenticated_user_test_1.data == loan_data
    assert serializer.data['payment_sum'] == 110
    assert isinstance(serializer.data['value'], float)


def test_retrieve_loan_from_other_client_not_found(auth_client_user_test_1, loan_02):
    """
    Certifies that a user can not retrieve
    loans from others.
    """
    resp = auth_client_user_test_1.get(f'/api/loans/{loan_02.pk}/')
    assert resp.status_code == HTTP_404_NOT_FOUND


def test_unauthenticated_user_can_not_retrieve_loans():
    """
    Certifies that non authenticated users can not
    retrieve loans.
    """
    client = APIClient()
    resp = client.get('/api/loans/')
    assert resp.status_code == HTTP_401_UNAUTHORIZED
