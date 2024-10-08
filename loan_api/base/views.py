from rest_framework import viewsets

from loan_api.base.loans import create_loan
from loan_api.base.models import Loan, Payment
from loan_api.base.payments import create_payment
from loan_api.base.serializers import LoanSerializer, PaymentSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from django.db.models import Sum


class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer

    def get_queryset(self):
        client = self.request.user
        return (Loan.objects.filter(client=client).
                annotate(sum=Sum('payments__value', default=0)).
                order_by('-request_date'))

    def create(self, request, *args, **kwargs):
        new_loan = create_loan(self.request)
        new_loan = LoanSerializer(new_loan)
        return Response(new_loan.data, status=HTTP_201_CREATED)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        client = self.request.user
        loan_id = self.request.query_params.get('loan')
        if loan_id is not None:
            return Payment.objects.filter(loan__client=client).filter(loan__id=loan_id).order_by('-payment_date')
        return Payment.objects.filter(loan__client=client).order_by('-payment_date')

    def create(self, request, *args, **kwargs):
        new_payment = create_payment(self.request)
        new_payment = PaymentSerializer(new_payment)
        return Response(new_payment.data, status=HTTP_201_CREATED)
