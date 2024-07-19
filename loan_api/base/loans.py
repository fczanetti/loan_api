from datetime import date
from decimal import Decimal

from loan_api.base.models import Loan, Payment
from django.db.models import Sum
from ipware import get_client_ip


def create_loan(request):
    """
    Receives a request and returns a Loan instance
    if the input was valid.
    """
    from loan_api.base.serializers import LoanSerializer

    # Creating a copy so data can be edited.
    data = request.data.copy()

    # Using django-ipware to get the ip address
    ip_address, _ = get_client_ip(request)

    # Get today's date as request_date if not informed
    request_date = data.get('request_date', date.today())
    if not request_date:  # Dealing with empty strings when inserted
        request_date = date.today()

    serializer = LoanSerializer(data=data)
    if serializer.is_valid(raise_exception=True):

        # Including ip_address and client when saving
        serializer.save(ip_address=ip_address,
                        client=request.user,
                        request_date=request_date)
        return serializer.instance


def calculate_installment_value(loan: Loan):
    """
    Calculates the value of each installment based
    on value, number of installments and interest
    rate of a loan.
    """
    # Original value of the loan
    ov = Decimal(loan.value)

    # Number of installments to quit the loan
    n = Decimal(loan.installments)

    # Interest rate agreed
    i = Decimal(loan.interest_rate) / Decimal('100')

    numerator = Decimal((((1 + i) ** n) * i))
    denominator = Decimal((((1 + i) ** n) - 1))

    # Value of monthly payment/installments
    iv = ov * numerator / denominator

    return round(iv, 2)


def calculate_unpaid_value(loan):
    """
    Calculates the total unpaid value for a loan
    discounting the amount already paid.
    """
    # Value of each installment
    installment_value = calculate_installment_value(loan)

    # Total value to be paid (original value + interest)
    total_value = installment_value * loan.installments

    # Retrieving what was already paid
    # When a Loan object is not serialized through a GET
    # request the attribute 'sum' is not created, that's
    # why this conditional was created. It happens in
    # some tests
    if hasattr(loan, 'sum'):
        return total_value - loan.sum
    paid_value = Payment.objects.filter(loan=loan).aggregate(Sum('value', default=0))['value__sum']
    return total_value - paid_value
