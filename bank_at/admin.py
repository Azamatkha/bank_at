from django.contrib import admin
from django.utils.timezone import localtime
from .models import BankAtResponseLog, CreditInfoUpdateLog


@admin.register(BankAtResponseLog)
class BankAtResponseLogAdmin(admin.ModelAdmin):

    list_display = ("id","credit_id","status","runtime")
    ordering = ("-id",)
    display_fields = ("credit_id","response_data","status","runtime")
    readonly_fields = ("credit_id","response_data","status","runtime")
    def runtime(self, obj):
        if obj.created_at:
            t = localtime(obj.created_at)
            return t.strftime("%Y-%m-%d %H:%M:%S")
        return "-"
    runtime.short_description = "Time"


@admin.register(CreditInfoUpdateLog)
class CreditInfoUpdateLogAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "runtime")
    display_fields = ("payload","status","runtime")
    readonly_fields = ("payload","status","runtime")
    def runtime(self, obj):
        if obj.created_at:
            t = localtime(obj.created_at)
            return t.strftime("%Y-%m-%d %H:%M:%S")
        return "-"
    runtime.short_description = "Time"