from django.urls import path
from .views import CreditInfoUpdateAPIView

urlpatterns = [
    path("credit-info-update/", CreditInfoUpdateAPIView.as_view()),
]
