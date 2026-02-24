from django.shortcuts import render
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CreditData, ResursRequestLog, PaymentRequestLog, PaymentQueue
from .serializers import CreditRequestSerializer, CreditResponseSerializer, PaymentCreateSerializer,PaymentResponseSerializer
from bank_at.models import BankAtResponseLog
from config.permissions import IsBankAt


class CreditInfoAPIView(APIView):
    permission_classes = [IsAuthenticated,IsBankAt]
    @swagger_auto_schema(
        operation_description="Kredit ma'lumotlarini olish",
        request_body=CreditRequestSerializer,
        responses={status.HTTP_200_OK: CreditResponseSerializer}
    )
    def post(self, request):
        serializer = CreditRequestSerializer(data=request.data)
        if not serializer.is_valid():
            ResursRequestLog.objects.create(
                credit_id=request.data.get("credit_id"),
                pnfl=request.data.get("pnfl"),
                status=status.HTTP_400_BAD_REQUEST
            )
            return Response(
                {"error": "Invalid request",
                 "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        credit_id = serializer.validated_data.get("credit_id")
        pnfl = serializer.validated_data.get("pnfl")
        try:
            credit = CreditData.objects.get(
                credit_id=credit_id,
                loan_pnfl=pnfl
            )
        except CreditData.DoesNotExist:
            ResursRequestLog.objects.create(
                credit_id=credit_id,
                pnfl=pnfl,
                status=status.HTTP_204_NO_CONTENT
            )
            return Response(
                {"error": "Berilgan credit id bo'yicha ma'lumot topilmadi!"},
                status=status.HTTP_204_NO_CONTENT
            )
        response_serializer = CreditResponseSerializer(credit)
        response_data = response_serializer.data
        ResursRequestLog.objects.create(
            credit_id=credit_id,
            pnfl=pnfl,
            status=status.HTTP_200_OK
        )
        BankAtResponseLog.objects.create(
            credit_id=credit_id,
            response_data=response_data,
            status=status.HTTP_200_OK
        )
        return Response(response_data, status=status.HTTP_200_OK)


class PaymentCreateAPIView(APIView):
    permission_classes = []
    @swagger_auto_schema(
        operation_description="User kredit to‘lovi",
        request_body=PaymentCreateSerializer,
        responses={201: PaymentResponseSerializer}
    )
    def post(self, request):

        serializer = PaymentCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"error": "Invalid request", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        credit_id = serializer.validated_data["credit_id"]
        paid_amount = serializer.validated_data["paid_amount"]

        try:
            credit = CreditData.objects.get(credit_id=credit_id)
        except CreditData.DoesNotExist:
            return Response(
                {"error": "Credit topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )
        old_balance = int(credit.credit_balance.replace(" ", ""))
        paid_int = int(paid_amount.replace(" ", ""))
        new_balance = old_balance - paid_int
        if new_balance < 0:
            return Response(
                {"error": "To'lov balansdan katta"},
                status=status.HTTP_400_BAD_REQUEST
            )
        credit.credit_balance = str(new_balance)
        credit.save()
        PaymentQueue.objects.create(
            credit_id=credit_id,
            paid_amount=paid_amount
        )

        response_data = {
            "credit_id": credit_id,
            "paid_amount": paid_amount,
            "credit_balance": str(new_balance),
            "paid_percent_amount": credit.paid_precent_amount,
            "loan_paid_date": timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        PaymentRequestLog.objects.create(
            credit_id=credit_id,
            paid_amount=paid_amount,
            response_data=response_data,
            status=201
        )
        return Response(response_data, status=status.HTTP_201_CREATED)

