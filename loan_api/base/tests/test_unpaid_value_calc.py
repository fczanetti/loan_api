from decimal import Decimal

import pytest
from model_bakery import baker

from loan_api.base.loans import calculate_installment_value, calculate_unpaid_value
from loan_api.base.models import Loan, Payment


@pytest.fixture
def loan_test_calc(db):
    """
    Creates and returns a loan to test
    calculating unpaid value and installments.
    """
    loan = baker.make(Loan, value=30_000, interest_rate=1.5, installments=12)
    return loan


def test_installment_value(loan_test_calc):
    """
    Certifies that the installment value
    is calculated correctly.
    """
    installment_value = calculate_installment_value(loan_test_calc)
    assert installment_value == Decimal('2750.40')


def test_calc_unpaid_value(loan_test_calc):
    """
    Certifies that the unpaid value is
    calculated correctly.
    """
    baker.make(Payment, value=2_750.40, loan=loan_test_calc)
    unpaid_value = calculate_unpaid_value(loan_test_calc)
    assert unpaid_value == Decimal('30254.40')
