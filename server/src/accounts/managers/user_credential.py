from typing import Any, Optional, TypeVar, Type
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib import auth

T = TypeVar('T', bound='UserCredentialManager')

class UserCredentialManager(BaseUserManager):
    use_in_migrations: bool = True

    def _create_user_object(
        self: T,
        email: str,
        password: str,
        **extra_fields: Any
    ) -> Any:
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(
        self: T,
        email: str,
        password: str,
        **extra_fields: Any
    ) -> Any:
        user = self._create_user_object(email, password, **extra_fields)
        user.save(using=self._db)
        return user

    async def _acreate_user(
        self: T,
        email: str,
        password: str,
        **extra_fields: Any
    ) -> Any:
        user = self._create_user_object(email, password, **extra_fields)
        await user.asave(using=self._db)
        return user

    def create_user(
        self: T,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> Any:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    create_user.alters_data = True

    async def acreate_user(
        self: T,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> Any:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return await self._acreate_user(email, password, **extra_fields)

    acreate_user.alters_data = True

    def create_superuser(
        self: T,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> Any:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)

    create_superuser.alters_data = True

    async def acreate_superuser(
        self: T,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> Any:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return await self._acreate_user(email, password, **extra_fields)

    acreate_superuser.alters_data = True

    def with_perm(
        self: T,
        perm: str,
        is_active: bool = True,
        include_superusers: bool = True,
        backend: Optional[Any] = None,
        obj: Optional[Any] = None
    ) -> Any:
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
