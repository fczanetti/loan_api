import pytest

from loan_api.base.models import Loan
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient
from loan_api.base.serializers import LoanSerializer


@pytest.fixture
def resp_update_loan_authenticated_user_test_1(auth_client_user_test_1, loan_01, bank):
    """
    Creates a request updating a loan and returns a response.
    """
    data = {'value': 110, 'interest_rate': 2, 'bank': bank.pk}
    resp = auth_client_user_test_1.put(f'/api/loans/{loan_01.pk}/', data=data)
    return resp


def test_resp_status_code_update_loan(resp_update_loan_authenticated_user_test_1):
    """
    Certifies that the update returns a response
    with a 200 status code.
    """
    assert resp_update_loan_authenticated_user_test_1.status_code == HTTP_200_OK


def test_updated_loan_returned_in_response(resp_update_loan_authenticated_user_test_1):
    """
    Certifies that the loan updated is returned
    in the response.
    """
    loan = Loan.objects.filter(client='User Test 1').filter(value=110).first()
    serializer = LoanSerializer(loan)
    assert resp_update_loan_authenticated_user_test_1.json() == serializer.data


def test_user_1_can_not_update_loan_from_user_2(auth_client_user_test_1, loan_02, bank):
    """
    Certifies that a user can not update a loan that
    belongs to another user.
    """
    data = {'value': 110, 'interest_rate': 2, 'bank': bank.pk}
    resp = auth_client_user_test_1.put(f'/api/loans/{loan_02.pk}/', data=data)
    assert resp.status_code == HTTP_404_NOT_FOUND


def test_unauthenticated_user_can_not_update_loans(loan_01, bank):
    """
    Certifies that a non authenticated user can not
    update loans.
    """
    data = {'value': 110, 'interest_rate': 2, 'bank': bank.pk}
    client = APIClient()
    resp = client.put(f'/api/loans/{loan_01.pk}/', data=data)
    assert resp.status_code == HTTP_401_UNAUTHORIZED


def test_invalid_inputs_not_allowed(auth_client_user_test_1, loan_01, bank):
    """
    Certifies that invalid requests return a
    400 status code response.
    """
    data_01 = {'value': '', 'interest_rate': 2, 'bank': bank.pk}        # Invalid value
    data_02 = {'value': 120, 'interest_rate': 'a', 'bank': bank.pk}     # Invalid interest_rate
    data_03 = {'value': 120, 'interest_rate': 3, 'bank': 123}         # Invalid bank

    resp_01 = auth_client_user_test_1.put(f'/api/loans/{loan_01.pk}/', data=data_01)
    resp_02 = auth_client_user_test_1.put(f'/api/loans/{loan_01.pk}/', data=data_02)
    resp_03 = auth_client_user_test_1.put(f'/api/loans/{loan_01.pk}/', data=data_03)

    assert resp_01.status_code == HTTP_400_BAD_REQUEST
    assert resp_02.status_code == HTTP_400_BAD_REQUEST
    assert resp_03.status_code == HTTP_400_BAD_REQUEST


def test_ip_address_and_client_are_not_updated(bank, auth_client_user_test_1, loan_01):
    """
    Certifies that ip_address and client are not updated
    when inserted in a request.
    """
    loan_01.ip_address = '1.2.3.4'
    loan_01.save()
    data = {'value': 30, 'interest_rate': 2, 'bank': bank.pk, 'ip_address': 'new.ip.address', 'client': 'New Client'}
    resp = auth_client_user_test_1.put(f'/api/loans/{loan_01.pk}/', data=data)
    updated_loan = Loan.objects.get(ip_address='1.2.3.4')

    assert resp.status_code == HTTP_200_OK

    # Updated values
    assert updated_loan.value == 30
    assert updated_loan.interest_rate == 2

    # Values that should not be updated
    assert updated_loan.ip_address != 'new.ip.address'
    assert updated_loan.ip_address == '1.2.3.4'
    assert updated_loan.client != 'New Client'
    assert updated_loan.client == loan_01.client


def test_partial_update(auth_client_user_test_1, loan_01):
    """
    Certifies that partial updates are also allowed.
    """
    data = {'value': 199}
    resp = auth_client_user_test_1.put(f'/api/loans/{loan_01.pk}/', data=data)
    updated_loan = Loan.objects.get(id=loan_01.pk)

    assert resp.status_code == HTTP_200_OK
    assert updated_loan.value == 199
