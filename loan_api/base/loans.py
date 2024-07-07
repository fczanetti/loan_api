from loan_api.base.serializers import LoanSerializer


def create_loan(request):
    """
    Receives a request and returns a Loan instance
    if the input was valid.
    """

    # Creating a copy so data can be edited.
    data = request.data.copy()

    # Getting some necessary infos
    data['ip_address'] = request.stream.META.get('REMOTE_ADDR')
    data['client'] = request.user.username

    # Creating and returning a Loan instance
    serializer = LoanSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serializer.instance
