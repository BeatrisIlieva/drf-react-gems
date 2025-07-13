"""
User Photo Model for DRF React Gems E-commerce Platform

This module defines the UserPhoto model which handles user profile pictures.
It uses Cloudinary for image storage and management, providing automatic
image optimization, CDN delivery, and cloud storage capabilities.

The UserPhoto model:
- Stores user profile pictures in the cloud via Cloudinary
- Uses one-to-one relationship with the user model
- Provides automatic image optimization and transformation
- Enables efficient image delivery through CDN
"""

# Django imports for model functionality
from django.contrib.auth import get_user_model
from django.db import models

# Cloudinary integration for cloud-based image storage
from cloudinary.models import CloudinaryField

# Get the active user model (our custom UserCredential)
UserModel = get_user_model()


class UserPhoto(models.Model):
    """
    User photo model for storing profile pictures.
    
    This model handles user profile pictures using Cloudinary for storage.
    Cloudinary provides automatic image optimization, CDN delivery, and
    cloud storage, making it ideal for user-generated content.
    
    Features:
    - Cloud-based image storage with automatic backup
    - Automatic image optimization and compression
    - CDN delivery for fast image loading
    - Automatic image transformation (resize, crop, etc.)
    - One-to-one relationship with user model
    
    The photo field uses CloudinaryField which automatically handles:
    - Image upload to Cloudinary
    - Image optimization and compression
    - CDN URL generation
    - Image transformation parameters
    """
    
    # Cloudinary field for image storage
    # 'image' is the folder name in Cloudinary where images will be stored
    # null=True allows the field to be NULL in database (user can have no photo)
    # blank=False means the field cannot be empty in forms (must have a value if provided)
    photo = CloudinaryField(
        'image',      # Cloudinary folder name for organization
        null=True,    # Can be NULL in database
        blank=False,  # Cannot be empty string in forms
    )

    # One-to-one relationship with the user model
    # primary_key=True makes this the primary key, creating a direct relationship
    # on_delete=models.CASCADE means if the user is deleted, the photo is also deleted
    # This ensures data consistency and prevents orphaned photo records
    user = models.OneToOneField(
        to=UserModel,           # Link to the custom user model
        on_delete=models.CASCADE,  # Delete photo when user is deleted
        primary_key=True,       # Use this field as the primary key
    )
