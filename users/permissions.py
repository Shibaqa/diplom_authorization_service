from rest_framework.permissions import BasePermission


class IsCurrentUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj:

            return True

        return False
