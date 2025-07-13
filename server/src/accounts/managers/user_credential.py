"""
User Credential Manager for DRF React Gems E-commerce Platform

This module defines the custom user manager for the UserCredential model.
The manager extends Django's BaseUserManager to provide custom user creation
methods that work with our email-based authentication system.

The manager provides:
- Custom user creation with email as primary identifier
- Password hashing and security
- Superuser creation with proper permissions
- Async support for modern Django applications
- Permission-based user filtering

This manager is essential for Django's authentication system to work properly
with our custom user model.
"""

# Type hints for better code documentation and IDE support
from typing import Any, Optional, TypeVar, Type
# Django authentication imports for custom user management
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib import auth

# Type variable for the manager class (used for type hints)
T = TypeVar('T', bound='UserCredentialManager')


class UserCredentialManager(BaseUserManager):
    """
    Custom user manager for the UserCredential model.
    
    This manager extends Django's BaseUserManager to provide custom user creation
    methods that work with our email-based authentication system. It handles:
    - User creation with email as primary identifier
    - Password hashing and security
    - Superuser creation with proper permissions
    - Async support for modern Django applications
    
    The manager is used by Django's authentication system and provides
    the methods needed for user creation, management, and queries.
    """
    
    # Flag indicating this manager can be used in migrations
    # This is required for Django to use this manager during database migrations
    use_in_migrations: bool = True

    def _create_user_object(
        self: T,
        email: str,
        password: str,
        **extra_fields: Any
    ) -> Any:
        """
        Create a user object without saving it to the database.
        
        This is a private method that creates the user object in memory
        but doesn't save it. It's used by other methods that need to
        create users with different save strategies (sync/async).
        
        Args:
            email: User's email address (primary identifier)
            password: User's password (will be hashed)
            **extra_fields: Additional fields for the user model
        
        Returns:
            UserCredential object (not saved to database)
        
        Raises:
            ValueError: If email is not provided
        """
        # Validate that email is provided
        if not email:
            raise ValueError("The given email must be set")
        
        # Normalize email (convert to lowercase, etc.)
        email = self.normalize_email(email)
        
        # Create user object with email and extra fields
        user = self.model(email=email, **extra_fields)
        
        # Hash the password for security
        user.password = make_password(password)
        
        return user

    def _create_user(
        self: T,
        email: str,
        password: str,
        **extra_fields: Any
    ) -> Any:
        """
        Create and save a regular user to the database.
        
        This is a private method that creates a user object and saves it
        to the database synchronously. It's used by create_user().
        
        Args:
            email: User's email address
            password: User's password
            **extra_fields: Additional fields for the user model
        
        Returns:
            Saved UserCredential object
        """
        # Create user object without saving
        user = self._create_user_object(email, password, **extra_fields)
        
        # Save to database using the manager's database
        user.save(using=self._db)
        
        return user

    async def _acreate_user(
        self: T,
        email: str,
        password: str,
        **extra_fields: Any
    ) -> Any:
        """
        Create and save a regular user to the database asynchronously.
        
        This is an async version of _create_user for use in async Django
        applications. It provides the same functionality but uses async/await.
        
        Args:
            email: User's email address
            password: User's password
            **extra_fields: Additional fields for the user model
        
        Returns:
            Saved UserCredential object
        """
        # Create user object without saving
        user = self._create_user_object(email, password, **extra_fields)
        
        # Save to database asynchronously
        await user.asave(using=self._db)
        
        return user

    def create_user(
        self: T,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> Any:
        """
        Create and save a regular user.
        
        This is the main method for creating regular users. It sets default
        values for staff and superuser flags and calls the private creation method.
        
        Args:
            email: User's email address
            password: User's password
            **extra_fields: Additional fields for the user model
        
        Returns:
            Saved UserCredential object
        
        Example:
            user = UserCredential.objects.create_user(
                email='user@example.com',
                password='secure_password',
                username='john_doe'
            )
        """
        # Set default values for regular users
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        
        # Create and save the user
        return self._create_user(email, password, **extra_fields)

    # Flag indicating this method modifies database data
    # Used by Django for transaction management
    create_user.alters_data = True

    async def acreate_user(
        self: T,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> Any:
        """
        Create and save a regular user asynchronously.
        
        Async version of create_user for use in async Django applications.
        
        Args:
            email: User's email address
            password: User's password
            **extra_fields: Additional fields for the user model
        
        Returns:
            Saved UserCredential object
        """
        # Set default values for regular users
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        
        # Create and save the user asynchronously
        return await self._acreate_user(email, password, **extra_fields)

    # Flag indicating this method modifies database data
    acreate_user.alters_data = True

    def create_superuser(
        self: T,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> Any:
        """
        Create and save a superuser.
        
        This method creates a user with administrative privileges. It ensures
        that superusers have the proper staff and superuser flags set.
        
        Args:
            email: User's email address
            password: User's password
            **extra_fields: Additional fields for the user model
        
        Returns:
            Saved UserCredential object with admin privileges
        
        Raises:
            ValueError: If is_staff or is_superuser is not True
        
        Example:
            admin = UserCredential.objects.create_superuser(
                email='admin@example.com',
                password='admin_password'
            )
        """
        # Set default values for superusers
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        # Validate that superuser has proper privileges
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        # Create and save the superuser
        return self._create_user(email, password, **extra_fields)

    # Flag indicating this method modifies database data
    create_superuser.alters_data = True

    async def acreate_superuser(
        self: T,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> Any:
        """
        Create and save a superuser asynchronously.
        
        Async version of create_superuser for use in async Django applications.
        
        Args:
            email: User's email address
            password: User's password
            **extra_fields: Additional fields for the user model
        
        Returns:
            Saved UserCredential object with admin privileges
        
        Raises:
            ValueError: If is_staff or is_superuser is not True
        """
        # Set default values for superusers
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        # Validate that superuser has proper privileges
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        # Create and save the superuser asynchronously
        return await self._acreate_user(email, password, **extra_fields)

    # Flag indicating this method modifies database data
    acreate_superuser.alters_data = True

    def with_perm(
        self: T,
        perm: str,
        is_active: bool = True,
        include_superusers: bool = True,
        backend: Optional[Any] = None,
        obj: Optional[Any] = None
    ) -> Any:
        """
        Return users with the specified permission.
        
        This method filters users based on their permissions. It's useful
        for finding users with specific capabilities or roles.
        
        Args:
            perm: Permission string (e.g., 'auth.add_user')
            is_active: Whether to include only active users
            include_superusers: Whether to include superusers
            backend: Authentication backend to use
            obj: Object to check permissions against
        
        Returns:
            QuerySet of users with the specified permission
        
        Raises:
            ValueError: If multiple backends are configured and backend not specified
            TypeError: If backend is not a string
        """
        # Handle backend selection
        if backend is None:
            # Get all configured authentication backends
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                # If only one backend, use it
                backend, _ = backends[0]
            else:
                # If multiple backends, require explicit backend specification
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            # Validate backend is a string
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            # Load the backend from string
            backend = auth.load_backend(backend)
        
        # Use backend's with_perm method if available
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        
        # Return empty queryset if backend doesn't support with_perm
        return self.none()
