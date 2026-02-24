from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CreditInfoUpdateLog
from bank_resurs_at.models import PaymentQueue, CreditData
from config.permissions import IsResurs
import threading
import time


worker_started = False
def background_sender():
    while True:
        qs = PaymentQueue.objects.filter(sent=False).order_by("created_at")
        items = []
        for p in qs:
            try:
                credit = CreditData.objects.get(credit_id=p.credit_id)
            except CreditData.DoesNotExist:
                continue
            items.append({
                "credit_id": p.credit_id,
                "paid_amount": p.paid_amount,
                "credit_balance": credit.credit_balance,
                "paid_percent_amount": credit.paid_precent_amount
            })
        if items:
            CreditInfoUpdateLog.objects.create(
                payload={"items": items},
                status=200
            )
            qs.update(sent=True)
        time.sleep(60)

class CreditInfoUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsResurs]

    @swagger_auto_schema(operation_description="Online POST /credit-info-update/ metodi")
    def post(self, request):
        global worker_started
        if not worker_started:
            thread = threading.Thread(target=background_sender, daemon=True)
            thread.start()
            worker_started = True
        data = request.data
        CreditInfoUpdateLog.objects.create(
            payload=data,
            status=200
        )
        return Response({"message": "Update qabul qilindi"}, status=status.HTTP_200_OK)