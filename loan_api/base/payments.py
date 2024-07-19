from datetime import date

from loan_api.base.serializers import PaymentSerializer


def create_payment(request):
    """
    Creates and returns a Payment.
    """
    data = request.data.copy()

    # Insert payment_date if not informed
    payment_date = data.get('payment_date', date.today())
    if not payment_date:  # Dealing with empty strings when inserted
        payment_date = date.today()

    # As the create method was overridden in PaymentViewSet, the context
    # has to be informed in this PaymentSerializer instance. If we don't
    # inform, it won't be possible to get the client from the context in
    # validate_loan method from PaymentSerializer, because the context
    # will be empty
    serializer = PaymentSerializer(data=data, context={'request': request})
    if serializer.is_valid(raise_exception=True):
        serializer.save(payment_date=payment_date)
        return serializer.instance
