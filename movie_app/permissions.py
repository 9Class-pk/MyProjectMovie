from rest_framework import permissions

class CheckStatus(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.status == 'pro':
            return True
        if request.user.status == 'simple' and obj.status_movie == 'simple':
            return True
        return False


class CheckRating(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.status == 'pro':
            return True
        return False

