from django.contrib import admin
from django.utils.timezone import localtime

from .admin_site import resurs_admin_site
from .models import CreditData, ResursRequestLog, PaymentRequestLog, PaymentQueue

class CreditDataAdmin(admin.ModelAdmin):
    list_display = (
        "credit_id", "loan_person_name", "loan_pnfl", "region",
        "contract_summ", "credit_balance", "type_of_credit"
    )
    ordering = ("-credit_id",)
    search_fields = ("credit_id", "loan_pnfl", "loan_person_name")

    def get_queryset(self, request):
        return super().get_queryset(request)

    def save_model(self, request, obj, form, change):
        obj.save()

    def delete_model(self, request, obj):
        obj.delete


class ResursRequestLogAdmin(admin.ModelAdmin):

    list_display = ( "id","credit_id","pnfl","status","runtime")
    ordering = ("-id",)
    readonly_fields = ("credit_id","pnfl","status","runtime")

    def get_queryset(self, request):
        return super().get_queryset(request)

    def runtime(self, obj):
        if obj.created_at:
            t = localtime(obj.created_at)
            return t.strftime("%Y-%m-%d %H:%M:%S")
        return "-"
    runtime.short_description = "Time"

class PaymentQueueAdmin(admin.ModelAdmin):

    list_display = ("credit_id", "paid_amount", "sent", "runtime")
    list_filter = ("sent","credit_id")
    search_fields = ("credit_id",)
    ordering = ("-id",)
    display_fields = ("credit_id", "paid_amount", "sent", "runtime")
    def get_queryset(self, request):
        return super().get_queryset(request)

    def runtime(self, obj):
        if obj.created_at:
            t = localtime(obj.created_at)
            return t.strftime("%Y-%m-%d %H:%M:%S")
        return "-"
    runtime.short_description = "Created At"

class PaymentRequestLogAdmin(admin.ModelAdmin):

    list_display = ("credit_id", "paid_amount", "status", "runtime")
    ordering = ("-id",)
    readonly_fields = ("credit_id", "paid_amount", "response_data", "status", "runtime")

    def get_queryset(self, request):
        return super().get_queryset(request)

    def runtime(self, obj):
        if obj.created_at:
            t = localtime(obj.created_at)
            return t.strftime("%Y-%m-%d %H:%M:%S")
        return "-"
    runtime.short_description = "Time"

resurs_admin_site.register(CreditData, CreditDataAdmin)
resurs_admin_site.register(ResursRequestLog, ResursRequestLogAdmin)
resurs_admin_site.register(PaymentQueue, PaymentQueueAdmin)
resurs_admin_site.register(PaymentRequestLog, PaymentRequestLogAdmin)