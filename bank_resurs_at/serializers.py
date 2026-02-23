from rest_framework import serializers
from .models import CreditData

class CreditRequestSerializer(serializers.Serializer):
    pnfl = serializers.CharField(max_length=14)
    credit_id = serializers.CharField(max_length=10)

class CreditResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditData
        fields = "__all__"

class PaymentCreateSerializer(serializers.Serializer):
    credit_id = serializers.CharField(max_length=10)
    paid_amount = serializers.CharField(max_length=20)


class PaymentResponseSerializer(serializers.Serializer):
    credit_id = serializers.CharField()
    paid_amount = serializers.CharField()
    credit_balance = serializers.CharField()
    paid_percent_amount = serializers.CharField()
    loan_paid_date = serializers.CharField()