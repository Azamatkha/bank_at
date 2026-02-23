from rest_framework import serializers

class CreditRequestSerializer(serializers.Serializer):
    credit_id = serializers.CharField(max_length=10)
    pnfl = serializers.CharField(max_length=14)
