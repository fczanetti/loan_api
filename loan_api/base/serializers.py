from rest_framework import serializers

from loan_api.base.models import Loan


class LoanSerializer(serializers.HyperlinkedModelSerializer):
    bank = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'value', 'interest_rate', 'ip_address', 'request_date', 'bank', 'client']
