from datetime import date

import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from loan_api.base.models import Loan
from loan_api.base.serializers import LoanSerializer
from rest_framework.test import APIClient


@pytest.fixture
def resp_loan_creation_authenticated_user_test_1(auth_client_user_test_1, bank):
    """
    Creates a POST request by user named 'User Test 1' creating
    a new loan and returns a response.
    """
    data = {'value': 100, 'interest_rate': 5, 'bank': bank.pk, 'installments': 1}
    resp = auth_client_user_test_1.post('/api/loans/', data=data)
    return resp


def test_loan_creation_status_code(resp_loan_creation_authenticated_user_test_1):
    """
    Certifies that the status code returned from
    the request is 201 (created).
    """
    assert resp_loan_creation_authenticated_user_test_1.status_code == HTTP_201_CREATED


def test_new_loan_created(resp_loan_creation_authenticated_user_test_1):
    """
    Certifies that the new loan was created, saved and
    is shown in the response.
    """
    new_loan = Loan.objects.filter(client='user_01@email.com')
    assert new_loan.exists()

    serializer = LoanSerializer(new_loan.first())
    assert resp_loan_creation_authenticated_user_test_1.json() == serializer.data

    # Certifying ip_address and client were automatically
    # filled (these are not required in the request)
    assert serializer.data['ip_address'] != ''
    assert serializer.data['client'] != ''


def test_requests_with_invalid_data(auth_client_user_test_1, bank):
    """
    Certifies that a response with status code 400
    is returned if invalid values are filled or if
    fields are missing.
    Also certifies that extra fields informed are
    just ignored.
    """
    # Value must be positive
    data_01 = {'value': -1, 'interest_rate': 5, 'bank': bank.pk, 'installments': 1}
    # Interest rate must be a valid number
    data_02 = {'value': 1, 'interest_rate': '', 'bank': bank.pk, 'installments': 1}
    # The bank.pk must be valid (from an existing bank)
    data_03 = {'value': 1, 'interest_rate': 5, 'bank': 123, 'installments': 1}
    # bank.pk must not be null
    data_04 = {'value': 1, 'interest_rate': 5, 'installments': 1}
    # Extra fields are ignored
    data_05 = {'value': 1, 'interest_rate': 5, 'bank': bank.pk, 'extra_field': 'abc', 'installments': 1}
    # Value must have no more than 2 decimal places
    data_06 = {'value': 1.333, 'interest_rate': 5, 'bank': bank.pk, 'installments': 1}

    resp_01 = auth_client_user_test_1.post('/api/loans/', data=data_01)
    resp_02 = auth_client_user_test_1.post('/api/loans/', data=data_02)
    resp_03 = auth_client_user_test_1.post('/api/loans/', data=data_03)
    resp_04 = auth_client_user_test_1.post('/api/loans/', data=data_04)
    resp_05 = auth_client_user_test_1.post('/api/loans/', data=data_05)
    resp_06 = auth_client_user_test_1.post('/api/loans/', data=data_06)

    assert resp_01.status_code == HTTP_400_BAD_REQUEST
    assert resp_02.status_code == HTTP_400_BAD_REQUEST
    assert resp_03.status_code == HTTP_400_BAD_REQUEST
    assert resp_04.status_code == HTTP_400_BAD_REQUEST
    assert resp_05.status_code == HTTP_201_CREATED
    assert resp_06.status_code == HTTP_400_BAD_REQUEST


def test_unauthenticated_user_can_not_create_loan():
    """
    Certifies unauthenticated users can not
    create loans.
    :return:
    """
    client = APIClient()
    resp = client.get('/api/loans/')
    assert resp.status_code == HTTP_401_UNAUTHORIZED


def test_request_date_equals_today_if_not_filled(auth_client_user_test_1, bank):
    """
    Certifies that, if not informed, the request_date
    is equal the day of creation of the Loan.
    """
    data = {'value': 100, 'interest_rate': 5, 'bank': bank.pk, 'installments': 1}
    resp = auth_client_user_test_1.post('/api/loans/', data=data)
    today = date.today()
    assert resp.data['request_date'] == today.isoformat()
