from django.db import models

class CreditData(models.Model):
    credit_id = models.CharField(max_length=10, unique=True)
    bank_mfo = models.IntegerField()
    bank_name = models.CharField(max_length=150)
    loan_person_name = models.CharField(max_length=150)
    loan_pnfl = models.CharField(max_length=14)
    pas_series_number = models.CharField(max_length=9)
    tin = models.IntegerField()
    region = models.CharField(max_length=150)
    district = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    date_of_contract = models.CharField(max_length=10)
    loan_allocated_date = models.DateField()
    contract_end_date = models.DateField()
    contract_number = models.CharField(max_length=10)
    contract_summ = models.CharField(max_length=20)
    disbursed_loan_amount = models.CharField(max_length=20)
    loan_interest_rate = models.CharField(max_length=20)
    credit_balance = models.CharField(max_length=20)
    paid_precent_amount = models.CharField(max_length=20)
    cadastral_number = models.CharField(max_length=30)
    type_of_supply = models.CharField(max_length=150)
    credit_provision_amount = models.CharField(max_length=150)
    tin_of_company = models.CharField(max_length=9)
    name_of_company = models.CharField(max_length=150)
    type_of_credit = models.CharField(max_length=150)

    def __str__(self):
        return self.credit_id

class ResursRequestLog(models.Model):
    credit_id = models.CharField(max_length=20)
    pnfl = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Log POST/credit-info/  | {self.id}"

class PaymentQueue(models.Model):
    credit_id = models.CharField(max_length=20)
    paid_amount = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.credit_id} | {self.paid_amount}"

class PaymentRequestLog(models.Model):
    credit_id = models.CharField(max_length=20)
    paid_amount = models.CharField(max_length=20)
    response_data = models.JSONField()
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log POST/credit-info-update/  | {self.id}"