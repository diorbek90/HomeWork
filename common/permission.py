from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user and request.user.is_authenticated
        )


class IsSuperUser(BasePermission):
  
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsStaff(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
