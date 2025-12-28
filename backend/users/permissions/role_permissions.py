from rest_framework.permissions import BasePermission

ROLE_HIERARCHY = {
    "WAITER": 1,
    "CASHIER": 2,
    "MANAGER": 3,
}

class HasRole(BasePermission):
    required_role = None

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        groups = user.groups.all()
        if not groups.exists():
            return False

        # Determine highest role user has
        user_roles = []
        for group in groups:
            role = group.name.upper()
            if role in ROLE_HIERARCHY:
                user_roles.append(ROLE_HIERARCHY[role])

        if not user_roles:
            return False

        return max(user_roles) >= ROLE_HIERARCHY[self.required_role]


class IsWaiter(HasRole):
    required_role = "WAITER"


class IsCashier(HasRole):
    required_role = "CASHIER"


class IsManager(HasRole):
    required_role = "MANAGER"
