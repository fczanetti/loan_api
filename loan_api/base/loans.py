from loan_api.base.serializers import LoanSerializer


def create_loan(request):
    """
    Receives a request and returns a Loan instance
    if the input was valid.
    """
    # Creating a copy so data can be edited.
    data = request.data.copy()

    serializer = LoanSerializer(data=data)
    if serializer.is_valid(raise_exception=True):

        # Including ip_address and client when saving
        serializer.save(ip_address=request.stream.META.get('REMOTE_ADDR'),
                        client=request.user.username)
        return serializer.instance
