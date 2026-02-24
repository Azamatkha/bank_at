"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# ===== AUTO PUSH WORKER =====
import threading
import time
import requests
from django.db import close_old_connections
from bank_resurs_at.models import PaymentQueue, CreditData

BASE_URL = os.environ.get("BASE_URL", "https://bank-at.onrender.com")
BANK_AT_URL = f"{BASE_URL}/api/v1/bank/credit-info-update/"

def push_loop():
    print("AUTO PUSH WORKER STARTED")

    while True:
        try:
            close_old_connections()

            qs = PaymentQueue.objects.filter(sent=False).order_by("created_at")

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

            r = requests.post(BANK_AT_URL, json=payload, timeout=60)

            if r.status_code == 200 and items:
                qs.update(sent=True)

            print("PUSH OK:", r.status_code)

        except Exception as e:
            print("PUSH ERROR:", e)

        time.sleep(120)  # 2 minut


threading.Thread(target=push_loop, daemon=True).start()