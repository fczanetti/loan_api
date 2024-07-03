import pytest
from rest_framework.status import HTTP_201_CREATED
from loan_api.base.models import Bank, Loan
from loan_api.base.serializers import LoanSerializer


@pytest.fixture
def resp_loan_creation_authenticated_user_test_1(auth_client_user_test_1):
    """
    Creates a POST request by user named 'User Test 1' creating
    a new loan and returns a response.
    """
    bank = Bank.objects.create(name='Test Bank')
    data = {'value': 100, 'interest_rate': 5, 'bank': bank.pk}
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
    new_loan = Loan.objects.filter(value=100)
    assert new_loan.exists()

    serializer = LoanSerializer(new_loan.first())
    assert resp_loan_creation_authenticated_user_test_1.json() == serializer.data
