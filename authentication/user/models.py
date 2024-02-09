from django.db import models
from .managers import CustomUserManager
from .common import UserommonFields
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class CustomUser(UserommonFields, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
