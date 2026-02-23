from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CreditInfoUpdateLog
from config.permissions import IsResurs


class CreditInfoUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated,IsResurs]
    @swagger_auto_schema(operation_description="Online POST /credit-info-update/ metodi",)
    def post(self, request):
        data = request.data
        CreditInfoUpdateLog.objects.create(
            payload=data,
            status=200
        )
        return Response({"message": "Update qabul qilindi"}, status=status.HTTP_200_OK)