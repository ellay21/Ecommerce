from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Allows full access to admin users, but read-only access to others.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.role == 'admin'

class IsOwnerOrAdmin(BasePermission):
    """
    Allows access only to the admin or the owner of the object.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.owner == request.user