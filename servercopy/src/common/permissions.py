from rest_framework.permissions import BasePermission


class IsOrderManager(BasePermission):
    """
    Custom permission to allow only order managers to access review management.
    """

    def has_permission(self, request, view):
        # Check if user has the 'approve_review' permission
        # This permission is granted to users in the 'Reviewer' group
        return request.user.has_perm('products.approve_review')
