from rest_framework import serializers


def positive_value(value):
    """
    Return a ValidationError if the value
    informed is not positive.
    """
    if not value > 0:
        raise serializers.ValidationError('Make sure you informed a positive value.')
    return value


def non_negative_interest_rate(value):
    """
    Return a ValidationError if the interest_rate
    informed is negative.
    """
    if not value >= 0:
        raise serializers.ValidationError('Negative interest rates are not allowed.')
    return value
