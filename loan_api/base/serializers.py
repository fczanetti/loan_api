from rest_framework import serializers

from loan_api.base.models import Loan, Bank


class LoanSerializer(serializers.HyperlinkedModelSerializer):
    bank = serializers.PrimaryKeyRelatedField(queryset=Bank.objects.all())

    class Meta:
        model = Loan
        fields = ['id', 'value', 'interest_rate', 'ip_address', 'request_date', 'bank', 'client']
