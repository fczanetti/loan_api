from loan_api.base.models import Loan
from loan_api.base.serializers import LoanSerializer
from django.shortcuts import get_object_or_404


def create_loan(request):
    """
    Receives a request and returns a Loan instance
    if the input was valid.
    """

    # Creating a copy so data can be edited.
    data = request.data.copy()

    # Getting some necessary infos. If ip_address and client
    # are filled in the request they will be ignored and the
    # correct values will be these
    data['ip_address'] = request.stream.META.get('REMOTE_ADDR')
    data['client'] = request.user.username

    # Creating and returning a Loan instance
    serializer = LoanSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serializer.instance


def update_loan(request, pk):
    loan = get_object_or_404(Loan, pk=pk, client=request.user.username)

    data = request.data.copy()

    # Remove ip_address and client from data if filled, so
    # it is not intentionally updated by a user.
    data.pop('ip_address', None)
    data.pop('client', None)

    serializer = LoanSerializer(loan, data=data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serializer.instance
