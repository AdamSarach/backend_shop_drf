from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

'''Own permissions i.e. for model owner or selected group'''


class IsOrderOwner(permissions.BasePermission):
    message = "Not an owner."

    def has_object_permission(self, request, view, obj):
        return request.user == obj.or_username


class IsEmployeeGroup(permissions.BasePermission):
    message = "Not an employee."

    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='employee'):
            return True
        return False


class IsCustomerGroup(permissions.BasePermission):
    message = "Not a customer."

    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='customer'):
            return True
        return False


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
