import pytest
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK
from model_bakery import baker
from loan_api.base.models import Loan
from loan_api.base.serializers import LoanSerializer


@pytest.fixture
def loans(db):
    """
    Creates 2 loans.
    """
    return baker.make(Loan, _quantity=2)


@pytest.fixture
def resp_list_loans(loans):
    """
    Creates a request and returns its response.
    """
    client = APIClient()
    resp = client.get('/api/loans/')
    return resp


def test_resp_loans_status_code(resp_list_loans):
    """
    Certifies that the request to list loans is successfull
    and returns a 200 status code.
    """
    assert resp_list_loans.status_code == HTTP_200_OK


def test_loans_present_in_response(resp_list_loans):
    """
    Certifies that the loans created are present in
    the response.
    """
    loans = Loan.objects.all()
    for loan in loans:
        serializer = LoanSerializer(loan)
        assert serializer.data in resp_list_loans.json()['results']
