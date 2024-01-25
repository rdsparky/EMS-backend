from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from common.models import BaseModel
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta


class MyUserManager(BaseUserManager):
    """The Custom BaseManager Class"""

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email
        """
        user = self.create_user(email, password=password)
        user.is_super_user = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseModel):
    """
    User model with email and password as a login credentials
    """

    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=False, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_super_user = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        """
        String representation of name
        :return:
        """
        return "{}-{}-{}".format(
            self.first_name,
            self.last_name,
            self.email,
        )

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return True

    class Meta:
        """
        Verbose name and verbose plural
        """

        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]
        get_latest_by = "created_at"

    """
    To create a new instance of User model
    """
    """
    For retrieving tokens from simple-jwt
    """

    def tokens(self, remember_me=False):
        refresh = RefreshToken.for_user(self)
        if remember_me:
            refresh.set_exp(lifetime=timedelta(minutes=10))
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
