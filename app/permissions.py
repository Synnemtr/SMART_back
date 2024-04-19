from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to access to it.
    Assumes the model instance has an `is_owner` method.
    """

    def has_object_permission(self, request, view, obj):
        # Instance must have a method named `is_owner`.
        return obj.is_owner(request.user.id)


class UserCanOnlyRead(BasePermission):
    """
    Object-level permission to only allow owners of an object to access to it.
    """
    def has_permission(self, request, view):
        return request.method in ['GET', 'HEAD', 'OPTIONS'] and not request.user.is_staff


class UserDetailPermission(BasePermission):
    """
    """
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return obj.is_owner(request.user.id)
        elif request.method == 'PUT' or request.method == 'DELETE':
            return obj.is_owner(request.user.id) or request.user.is_staff
        else:
            return False
