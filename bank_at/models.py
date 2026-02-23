from django.db import models

class BankAtResponseLog(models.Model):
    credit_id = models.CharField(max_length=20, null=True, blank=True)
    response_data = models.JSONField(null=True, blank=True)
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log POST/credit-info/  | {self.id}"

class CreditInfoUpdateLog(models.Model):
    payload = models.JSONField()
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Log POST/credit-info-update/ | {self.id}"