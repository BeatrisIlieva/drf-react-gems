from rest_framework.permissions import BasePermission


class IsReviewer(BasePermission):
    """
    Custom permission to allow only reviewers to access review management.

    This permission class checks if the user has the 'approve_review' permission,
    which is granted to users in the 'Reviewer' group. Reviewers can:
    - View all reviews (approved and unapproved)
    - Approve/unapprove reviews
    - Regular users can only see approved reviews.
    """

    def has_permission(self, request, view):
        # Check if user has the 'approve_review' permission
        # This permission is granted to users in the 'Reviewer' group
        return request.user.has_perm('products.approve_review')
