from rest_framework import viewsets

from loan_api.base.loans import create_loan
from loan_api.base.models import Loan, Payment
from loan_api.base.serializers import LoanSerializer, PaymentSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED


class LoanViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LoanSerializer

    def get_queryset(self):
        user = self.request.user
        client = user.username
        return Loan.objects.filter(client=client).order_by('-request_date')

    def create(self, request, *args, **kwargs):
        new_loan = create_loan(self.request)
        new_loan = LoanSerializer(new_loan)
        return Response(new_loan.data, status=HTTP_201_CREATED)


class PaymentViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        client = user.username
        return Payment.objects.filter(loan__client=client).order_by('-payment_date')
