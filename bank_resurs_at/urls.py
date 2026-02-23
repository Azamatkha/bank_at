from django.urls import path
from .views import CreditInfoAPIView, PaymentCreateAPIView

urlpatterns = [
    path('credit-info/',CreditInfoAPIView.as_view()),
    path('payment/',PaymentCreateAPIView.as_view()),
]


