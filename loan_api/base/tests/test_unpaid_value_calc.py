from datetime import date
from decimal import Decimal

import pytest
from model_bakery import baker

from loan_api.base.loans import calculate_installment_value, calculate_unpaid_value
from loan_api.base.models import Loan, Payment


@pytest.fixture
def loan_test_calc_1(db):
    """
    Creates and returns a loan to test
    calculating unpaid value and installments.
    """
    loan = baker.make(Loan, value=30_000, interest_rate=1.5, installments=12, request_date=date.today())
    return loan


@pytest.fixture
def loan_test_calc_2(db):
    """
    Creates and returns a loan to test
    calculating unpaid value and installments.
    """
    loan = baker.make(Loan, value=10_588.36, interest_rate=1.47, installments=16, request_date=date.today())
    return loan


def test_installment_value(loan_test_calc_1, loan_test_calc_2):
    """
    Certifies that the installment value is calculated correctly.
    """
    installment_value_1 = calculate_installment_value(loan_test_calc_1)
    installment_value_2 = calculate_installment_value(loan_test_calc_2)
    assert installment_value_1 == Decimal('2750.40')
    assert installment_value_2 == Decimal('747.47')


def test_calc_unpaid_value(loan_test_calc_1, loan_test_calc_2):
    """
    Certifies that the unpaid value is calculated correctly.
    """
    baker.make(Payment, value=2_750.40, loan=loan_test_calc_1, payment_date=date.today())
    baker.make(Payment, value=747.47, loan=loan_test_calc_2, payment_date=date.today())
    unpaid_value_1 = calculate_unpaid_value(loan_test_calc_1)
    unpaid_value_2 = calculate_unpaid_value(loan_test_calc_2)
    assert unpaid_value_1 == Decimal('30254.40')
    assert unpaid_value_2 == Decimal('11212.05')
