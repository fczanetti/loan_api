from rest_framework import viewsets

from loan_api.base.loans import create_loan, update_loan
from loan_api.base.models import Loan, Payment
from loan_api.base.serializers import LoanSerializer, PaymentSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK


class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer

    def get_queryset(self):
        user = self.request.user
        client = user.username
        return Loan.objects.filter(client=client).order_by('-request_date')

    def create(self, request, *args, **kwargs):
        new_loan = create_loan(self.request)
        new_loan = LoanSerializer(new_loan)
        return Response(new_loan.data, status=HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        updated_loan = update_loan(self.request, kwargs['pk'])
        updated_loan = LoanSerializer(updated_loan)
        return Response(updated_loan.data, status=HTTP_200_OK)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        client = user.username
        return Payment.objects.filter(loan__client=client).order_by('-payment_date')
