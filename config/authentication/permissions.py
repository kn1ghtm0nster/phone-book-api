from rest_framework import permissions


def _in_group(user, name: str):
    return user.is_authenticated and user.groups.filter(name=name).exists()


class IsWriter(permissions.BasePermission):
    """
    Custom permission to only allow writers to edit objects.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser or _in_group(request.user, 'writer')


class IsReaderOrWriter(permissions.BasePermission):
    """
    Custom permission to verify if user is either reader or writer.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return _in_group(request.user, 'reader') or _in_group(request.user, 'writer')
