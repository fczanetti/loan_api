from rest_framework import serializers

from loan_api.base.models import Loan, Bank, Payment


class LoanSerializer(serializers.HyperlinkedModelSerializer):
    bank = serializers.PrimaryKeyRelatedField(queryset=Bank.objects.all())

    class Meta:
        model = Loan
        fields = ['id', 'value', 'interest_rate', 'ip_address', 'request_date', 'bank', 'client']


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    loan = serializers.PrimaryKeyRelatedField(queryset=Loan.objects.all())

    class Meta:
        model = Payment
        fields = ['id', 'loan', 'payment_date', 'value']
