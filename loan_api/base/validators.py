from rest_framework import serializers


def positive_value(value):
    """
    Return a ValidationError if the value
    informed is not positive.
    """
    if not value > 0:
        raise serializers.ValidationError('Make sure you informed a positive value.')
    return value
