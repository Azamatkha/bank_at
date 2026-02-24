import time
import requests
from django.core.management.base import BaseCommand
from bank_resurs_at.models import PaymentQueue, CreditData
import os

BASE_URL = os.environ.get("BASE_URL")
print(BASE_URL)
BANK_AT_URL = f"{BASE_URL}/api/v1/bank/credit-info-update/"
TOKEN_URL   = f"{BASE_URL}/api/v1/token/"
print(TOKEN_URL)
USERNAME    = "bank_resurs_at"
PASSWORD    = "Dj@ngo123"

def get_jwt():
    r = requests.post(TOKEN_URL, json={"username": USERNAME, "password": PASSWORD}, timeout=5)
    r.raise_for_status()
    return r.json()["access"]

class Command(BaseCommand):
    help = "Har 1 minutda paymentlarni yig‘ib bank_at ga yuboradi"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Update push loop started"))
        access_token = get_jwt()
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
                payload = {
                    "status": "PAYMENTS",
                    "count": len(items),
                    "items": items
                }
            else:
                payload = {
                    "status": "NOPAYMENT",
                    "message": "Ushbu oraliqda to'lov yo'q",
                }
            try:
                r = requests.post(
                    BANK_AT_URL,
                    json=payload,
                    headers={"Authorization": f"Bearer {access_token}"},
                    timeout=40
                )
                if r.status_code == 401:
                    access_token = get_jwt()
                    r = requests.post(
                        BANK_AT_URL,
                        json=payload,
                        headers={"Authorization": f"Bearer {access_token}"},
                        timeout=40
                    )
                ok = r.status_code == 200
            except Exception:
                ok = False
            if items and ok:
                qs.update(sent=True)
            time.sleep(120)