"""
This module defines the custom user manager for the UserCredential model.
The manager extends Django's BaseUserManager to provide custom user creation
methods that work with our email-based authentication system.
"""

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib import auth


class UserCredentialManager(BaseUserManager):
    """
    Custom user manager for the UserCredential model.

    This manager extends Django's BaseUserManager to provide custom user creation
    methods that work with our email-based authentication system. It handles:
    - User creation with email as primary identifier
    - Password hashing and security

    The manager is used by Django's authentication system and provides
    the methods needed for user creation, management, and queries.
    """

    use_in_migrations = True

    def _create_user_object(self, email, password, **extra_fields):
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
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)

        return user

    def _create_user(self, email, password, **extra_fields):
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
        user = self._create_user_object(email, password, **extra_fields)
        user.save(using=self._db)

        return user

    async def _acreate_user(self, email, password, **extra_fields):
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
        user = self._create_user_object(email, password, **extra_fields)
        await user.asave(using=self._db)

        return user

    def create_user(self, email, password, **extra_fields):
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
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    create_user.alters_data = True

    async def acreate_user(self, email, password, **extra_fields):
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
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return await self._acreate_user(email, password, **extra_fields)

    acreate_user.alters_data = True

    def create_superuser(self, email, password, **extra_fields):
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
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    create_superuser.alters_data = True

    async def acreate_superuser(self, email, password, **extra_fields):
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
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return await self._acreate_user(email, password, **extra_fields)

    acreate_superuser.alters_data = True

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
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
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )

        return self.none()
