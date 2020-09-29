from rest_framework.permissions import BasePermission


class OwnerOfResult(BasePermission):
    message = 'You must be user'
    def has_object_permission(self, request, view, obj):
        return obj.student_id.admin == request.user


