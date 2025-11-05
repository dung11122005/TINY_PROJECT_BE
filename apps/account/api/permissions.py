from rest_framework import permissions


class HasEndpointPermission(permissions.BasePermission):
    """
    Kiểm tra xem user có quyền truy cập endpoint + method không.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        # Superuser được phép tất cả
        if user.is_superuser:
            return True

        role = getattr(user, "role", None)
        if not role:
            return False

        path = request.path_info
        method = request.method.upper()

        # So khớp endpoint (chuẩn hóa)
        perms = role.permissions.filter(method=method)
        for perm in perms:
            if path.startswith(perm.endpoint):  # match kiểu prefix
                return True

        return False
