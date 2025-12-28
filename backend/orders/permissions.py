from rest_framework.permissions import BasePermission

class IsWaiterOrManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(
            name__in=['Waiter', 'Manager']
        ).exists()
