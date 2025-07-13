"""
Custom Permission Classes for DRF React Gems E-commerce Platform

This module defines custom permission classes for the e-commerce application.
These permissions provide fine-grained access control for different user roles
and business functions.

The permissions ensure that:
- Only authorized users can access specific functionality
- Role-based access control is properly enforced
- Security is maintained across the application
"""

from rest_framework.permissions import BasePermission


class IsReviewer(BasePermission):
    """
    Custom permission to allow only reviewers to access review management.
    
    This permission class checks if the user has the 'approve_review' permission,
    which is granted to users in the 'Reviewer' group. Reviewers can:
    - View all reviews (approved and unapproved)
    - Approve/unapprove reviews
    - Manage review content
    
    Regular users can only see approved reviews, while reviewers have
    full access to review management functionality.
    """
    
    def has_permission(self, request, view):
        """
        Check if the user has reviewer permissions.
        
        This method is called for every request to determine if the user
        has the necessary permissions to access the view. It checks if
        the user has the 'approve_review' permission, which is the
        defining permission for reviewers.
        
        Args:
            request: The HTTP request object
            view: The view being accessed
            
        Returns:
            bool: True if user has reviewer permissions, False otherwise
            
        Example:
            # User with reviewer permissions
            user.has_perm('products.approve_review')  # Returns True
            
            # Regular user
            user.has_perm('products.approve_review')  # Returns False
        """
        # Check if user has the 'approve_review' permission
        # This permission is granted to users in the 'Reviewer' group
        return request.user.has_perm('products.approve_review') 