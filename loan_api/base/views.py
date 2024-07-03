from rest_framework import viewsets

from loan_api.base.loans import create_loan
from loan_api.base.models import Loan
from loan_api.base.serializers import LoanSerializer
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
        return Loan.objects.filter(client=client).order_by('request_date')

    def create(self, request, *args, **kwargs):

        new_loan_data = create_loan(self.request)
        return Response(new_loan_data, status=HTTP_201_CREATED)
