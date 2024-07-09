import pytest
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient
from loan_api.base.models import Payment
from loan_api.base.serializers import PaymentSerializer


@pytest.fixture
def resp_update_payment_authenticated_user_1(auth_client_user_test_1, loan_01, payment_loan_01):
    """
    Creates a request updating a payment and returns a response.
    """
    data = {'loan': loan_01.pk, 'value': 123}
    resp = auth_client_user_test_1.put(f'/api/payments/{payment_loan_01.pk}/', data=data)
    return resp


def test_status_code_update_payment(resp_update_payment_authenticated_user_1):
    """
    Certifies that the response is successfull with a 200 status code.
    """
    assert resp_update_payment_authenticated_user_1.status_code == HTTP_200_OK


def test_payment_updated_and_returned_in_the_response(resp_update_payment_authenticated_user_1, payment_loan_01):
    """
    Certifies that the payment was updated and returned in the response.
    """
    payment = Payment.objects.get(id=payment_loan_01.pk)
    serializer = PaymentSerializer(payment)
    assert payment.value == 123
    assert resp_update_payment_authenticated_user_1.json() == serializer.data


def test_user_1_can_not_update_payment_from_user_2(auth_client_user_test_1, payment_loan_02, loan_01):
    """
    Certifies that a user can not update payments from others.
    """
    data = {'loan': loan_01.pk, 'value': 25}
    resp = auth_client_user_test_1.put(f'/api/payments/{payment_loan_02.pk}/', data=data)
    assert resp.status_code == HTTP_404_NOT_FOUND


def test_unauthenticated_users_can_not_update_payments(loan_01, payment_loan_01):
    """
    Certifies that non authenticated users can not update payments.
    """
    data = {'loan': loan_01.pk, 'value': 123}
    client = APIClient()
    resp = client.put(f'/api/payments/{payment_loan_01.pk}/', data=data)
    assert resp.status_code == HTTP_401_UNAUTHORIZED


def test_invalid_requests(auth_client_user_test_1, loan_01, loan_02, payment_loan_01):
    """
    Certifies invalid requests return a response with 400 status code.
    """
    data_1 = {'loan': loan_02.pk, 'value': 123}  # Trying to inform other user's loan ID
    data_2 = {'loan': '', 'value': 123}  # Not informing a loan ID
    data_3 = {'loan': loan_01.pk, 'value': ''}  # Not informing a value
    data_4 = {'loan': loan_01.pk, 'value': -10}  # Informing a negative value

    resp_1 = auth_client_user_test_1.put(f'/api/payments/{payment_loan_01.pk}/', data=data_1)
    resp_2 = auth_client_user_test_1.put(f'/api/payments/{payment_loan_01.pk}/', data=data_2)
    resp_3 = auth_client_user_test_1.put(f'/api/payments/{payment_loan_01.pk}/', data=data_3)
    resp_4 = auth_client_user_test_1.put(f'/api/payments/{payment_loan_01.pk}/', data=data_4)

    assert resp_1.status_code == HTTP_400_BAD_REQUEST
    assert resp_1.json()['loan'] == ['Make sure you informed a valid loan ID.']

    assert resp_2.status_code == HTTP_400_BAD_REQUEST
    assert resp_3.status_code == HTTP_400_BAD_REQUEST

    assert resp_4.status_code == HTTP_400_BAD_REQUEST
    assert resp_4.json()['value'] == ['Make sure you informed a greater than zero value.']
