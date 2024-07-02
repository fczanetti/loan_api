from rest_framework import viewsets
from loan_api.base.models import Loan
from loan_api.base.serializers import LoanSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all().order_by('request_date')
    serializer_class = LoanSerializer
