from rest_framework import serializers

from loan_api.base.loans import calculate_unpaid_value, calculate_installment_value
from loan_api.base.models import Loan, Bank, Payment
from django.db.models import Sum


class LoanSerializer(serializers.ModelSerializer):
    bank = serializers.PrimaryKeyRelatedField(queryset=Bank.objects.all())
    payment_sum = serializers.SerializerMethodField(read_only=True)
    unpaid_value = serializers.SerializerMethodField(read_only=True)
    installment_value = serializers.SerializerMethodField(read_only=True)
    client = serializers.PrimaryKeyRelatedField(source='client.email', read_only=True)

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
        # When a Loan object is not serialized through a GET
        # request the attribute 'sum' is not created, that's
        # why this conditional was created. It happens in
        # some tests
        if hasattr(obj, 'sum'):
            return obj.sum
        payment_sum = obj.payments.aggregate(Sum("value", default=0))['value__sum']
        return payment_sum

    def to_representation(self, instance):
        """
        Represent value as a float instead of string.
        """
        ret = super().to_representation(instance)
        ret['value'] = float(ret['value'])
        return ret


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
        client = self.context['request'].user
        if not Loan.objects.filter(client=client).filter(id=value.id).exists():
            raise serializers.ValidationError('Make sure you informed a valid loan ID.')
        return value

    def to_representation(self, instance):
        """
        Represent value as a float instead of string.
        """
        ret = super().to_representation(instance)
        ret['value'] = float(ret['value'])
        return ret
