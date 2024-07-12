from loan_api.base.models import Loan


def create_loan(request):
    """
    Receives a request and returns a Loan instance
    if the input was valid.
    """
    from loan_api.base.serializers import LoanSerializer

    # Creating a copy so data can be edited.
    data = request.data.copy()

    serializer = LoanSerializer(data=data)
    if serializer.is_valid(raise_exception=True):

        # Including ip_address and client when saving
        serializer.save(ip_address=request.stream.META.get('REMOTE_ADDR'),
                        client=request.user.email)
        return serializer.instance


def calculate_installment_value(loan: Loan):
    """
    Calculates the value of each installment based
    on value, number of installments and interest
    rate of a loan.
    """
    # Original value of the loan
    ov = loan.value

    # Number of installments to quit the loan
    n = loan.installments

    # Interest rate agreed
    i = loan.interest_rate / 100

    # Value of monthly payment/installments
    iv = ov * (((1 + i) ** n) * i) / (((1 + i) ** n) - 1)

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

    # paid_value = loan.payment_set.aggregate(Sum("value", default=0))['value__sum']
    paid_value = 0
    for payment in loan.payment_set.all():
        paid_value += payment.value

    return round(total_value - paid_value, 2)
