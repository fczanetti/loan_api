import pytest
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from loan_api.base.serializers import LoanSerializer


@pytest.fixture
def resp_list_loans_authenticated_user_test_1(loans, auth_client_user_test_1):
    """
    Creates a request by authenticated user named
    'User Test 1' and returns its response.
    """
    resp = auth_client_user_test_1.get('/api/loans/')
    return resp


def test_resp_loans_status_code(resp_list_loans_authenticated_user_test_1):
    """
    Certifies that the request to list loans is successfull
    and returns a 200 status code.
    """
    assert resp_list_loans_authenticated_user_test_1.status_code == HTTP_200_OK


def test_correct_loans_present_in_response(resp_list_loans_authenticated_user_test_1, loan_01, loan_02):
    """
    Certifies that only the loans from the user that made the request are present.
    """
    serializer_01 = LoanSerializer(loan_01)
    serializer_02 = LoanSerializer(loan_02)
    assert serializer_01.data in resp_list_loans_authenticated_user_test_1.data['results']
    assert serializer_02.data not in resp_list_loans_authenticated_user_test_1.data['results']


def test_unauthenticated_user_request_unauthorized(db):
    """
    Certifies that an unauthenticated user can not list loans.
    """
    client = APIClient()
    resp = client.get('/api/loans/')
    assert resp.status_code == HTTP_401_UNAUTHORIZED
