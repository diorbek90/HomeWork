from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    def has_object_permission(self, request, view):
        return request.user.is_authenticated
    

class IsAnonymousReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user and request.user.is_authenticated
    

class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff