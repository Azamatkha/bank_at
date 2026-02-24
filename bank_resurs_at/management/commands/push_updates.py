import time
import requests
import os
from django.core.management.base import BaseCommand
from bank_resurs_at.models import PaymentQueue, CreditData

BASE_URL = os.environ.get("BASE_URL", "https://bank-at.onrender.com")
BANK_AT_URL = f"{BASE_URL}/api/v1/bank/credit-info-update/"

class Command(BaseCommand):
    help = "Automatic push every 2 minutes"
    def handle(self, *args, **kwargs):
        self.stdout.write("Push worker started")
        while True:
            try:
                qs = PaymentQueue.objects.filter(sent=False)
                items = []
                for p in qs:
                    try:
                        credit = CreditData.objects.get(credit_id=p.credit_id)
                    except:
                        continue
                    items.append({
                        "credit_id": p.credit_id,
                        "paid_amount": p.paid_amount,
                        "credit_balance": credit.credit_balance,
                        "paid_percent_amount": credit.paid_precent_amount
                    })
                payload = {
                    "status": "PAYMENTS" if items else "NOPAYMENT",
                    "count": len(items),
                    "items": items
                }
                r = requests.post(
                    BANK_AT_URL,
                    json=payload,
                    timeout=60
                )
                if r.status_code == 200 and items:
                    qs.update(sent=True)
                print("Push sent:", r.status_code)
            except Exception as e:
                print("Push error:", e)

            time.sleep(120)