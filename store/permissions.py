from rest_framework import permissions
from rest_framework.request import Request


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

class ViewCustomerHistoryPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view):
        return request.user.has_perm('store.view_history')
#
# class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
#     def __init__(self):
#         self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
