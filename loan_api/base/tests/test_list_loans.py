import pytest
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from model_bakery import baker
from loan_api.base.models import Loan
from loan_api.base.serializers import LoanSerializer
from django.contrib.auth.models import User


@pytest.fixture
def users(db):
    """
    Creates and returns 2 users.
    """
    names = ['User Test 1', 'User Test 2']
    return [User.objects.create(username=name, password='userpass') for name in names]


@pytest.fixture
def loans(db, users):
    """
    Creates and returns 2 loans.
    """
    loans = [baker.make(Loan, client=f'{user.username} - {user.pk}') for user in users]
    return loans


@pytest.fixture
def resp_list_loans_authenticated_user_test_1(loans, users):
    """
    Creates a request by user named 'User Test 1' and returns its response.
    """
    user = User.objects.get(username='User Test 1')
    client = APIClient()
    client.force_authenticate(user=user)
    resp = client.get('/api/loans/')
    return resp


def test_resp_loans_status_code(resp_list_loans_authenticated_user_test_1):
    """
    Certifies that the request to list loans is successfull
    and returns a 200 status code.
    """
    assert resp_list_loans_authenticated_user_test_1.status_code == HTTP_200_OK


def test_correct_loans_present_in_response(resp_list_loans_authenticated_user_test_1):
    """
    Certifies that only the loans from the user that made the request are present.
    """
    user_01 = User.objects.get(username='User Test 1')
    user_02 = User.objects.get(username='User Test 2')
    loan_01 = Loan.objects.filter(client=f'{user_01.username} - {user_01.pk}').first()
    loan_02 = Loan.objects.filter(client=f'{user_02.username} - {user_02.pk}').first()
    serializer_01 = LoanSerializer(loan_01)
    serializer_02 = LoanSerializer(loan_02)
    assert serializer_01.data in resp_list_loans_authenticated_user_test_1.json()['results']
    assert serializer_02.data not in resp_list_loans_authenticated_user_test_1.json()['results']


def test_unauthenticated_user_request_unauthorized(db):
    """
    Certifies that an unauthenticated user can not list loans.
    """
    client = APIClient()
    resp = client.get('/api/loans/')
    assert resp.status_code == HTTP_401_UNAUTHORIZED
