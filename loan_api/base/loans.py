from loan_api.base.serializers import LoanSerializer


def create_loan(request):
    """
    Receives a request, validade the inputs via serializer,
    creates a new Loan and return the new Loan infos.
    :param request: The request to extract the input data from.
    :return: a dict with infos from the new Loan created.
    """

    # Creating a copy so data can be edited.
    data = request.data.copy()

    data['ip_address'] = request.stream.META.get('REMOTE_ADDR')
    data['bank'] = request.data.get('bank')
    data['client'] = request.user.username

    serializer = LoanSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
