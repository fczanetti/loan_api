from rest_framework import serializers

from loan_api.base.loans import calculate_unpaid_value, calculate_installment_value
from loan_api.base.models import Loan, Bank, Payment


class LoanSerializer(serializers.ModelSerializer):
    bank = serializers.PrimaryKeyRelatedField(queryset=Bank.objects.all())
    payment_sum = serializers.SerializerMethodField(read_only=True)
    unpaid_value = serializers.SerializerMethodField(read_only=True)
    installment_value = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'value', 'interest_rate', 'installments', 'installment_value',
                  'ip_address', 'request_date', 'bank', 'client', 'payment_sum', 'unpaid_value']
        read_only_fields = ['ip_address', 'client']

    def get_unpaid_value(self, obj):
        return calculate_unpaid_value(obj)

    def get_installment_value(self, obj):
        return calculate_installment_value(obj)

    def get_payment_sum(self, obj):
        # payment_sum = obj.payment_set.aggregate(Sum("value", default=0))['value__sum']
        payment_sum = 0
        for payment in obj.payment_set.all():
            payment_sum += payment.value
        return round(payment_sum, 2)


class PaymentSerializer(serializers.ModelSerializer):
    loan = serializers.PrimaryKeyRelatedField(queryset=Loan.objects.all())

    class Meta:
        model = Payment
        fields = ['id', 'loan', 'payment_date', 'value']

    def validate_loan(self, value):
        """
        Certifies that the loan informed belongs to
        the user creating the payment.
        """
        client = self.context['request'].user.email
        if not Loan.objects.filter(client=client).filter(id=value.id).exists():
            raise serializers.ValidationError('Make sure you informed a valid loan ID.')
        return value

    def validate_value(self, value):
        """
        Certifies that the value informed is positive.
        """
        if not value > 0:
            raise serializers.ValidationError('Make sure you informed a positive value.')
        return value
