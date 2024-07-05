from rest_framework import serializers

from loan_api.base.models import Loan, Bank, Payment


class LoanSerializer(serializers.HyperlinkedModelSerializer):
    bank = serializers.PrimaryKeyRelatedField(queryset=Bank.objects.all())
    payment_set = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'value', 'interest_rate', 'ip_address', 'request_date', 'bank', 'client', 'payment_set']
        read_only_fields = ['ip_address', 'client', 'payment_set']


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    loan = serializers.PrimaryKeyRelatedField(queryset=Loan.objects.all())

    class Meta:
        model = Payment
        fields = ['id', 'loan', 'payment_date', 'value']

    def validate_loan(self, value):
        """
        Certifies that the loan informed belongs to
        the user creating the payment.
        """
        client = self.context['request'].user.username
        if not Loan.objects.filter(client=client).filter(id=value.id).exists():
            raise serializers.ValidationError('Make sure you informed a valid loan ID.')
        return value
