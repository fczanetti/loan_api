from rest_framework import viewsets
from loan_api.base.models import Loan
from loan_api.base.serializers import LoanSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class LoanViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LoanSerializer

    def get_queryset(self):
        user = self.request.user
        client = f'{user.username} - {user.pk}'
        return Loan.objects.filter(client=client).order_by('request_date')
