from rest_framework.permissions import BasePermission

class IsBankAt(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.username == "bank_at"


class IsResurs(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.username == "bank_resurs_at"



