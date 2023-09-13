from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import pre_save
from django.dispatch import receiver

USER_TYPE_CHOICES = (
    ('merchant', 'Merchant'),
    ('admin', 'Admin'),
    ('vendor', 'Vendor')
)


class CustomAccountManager(BaseUserManager):
    def create_user(self, name, password, username, **other_fields):
        customer = self.model(name=name, password=password, username=username,
                              is_staff=other_fields.get("is_staff", False),
                              is_superuser=other_fields.get("is_superuser", False), is_active=True)
        customer.set_password(password)
        customer.save()
        return customer

    def create_superuser(self, name, password, username, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('merchant_id', 4000)
        other_fields.setdefault('type', 'admin')
        return self.create_user(name, password, username, **other_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    type = models.CharField(choices=USER_TYPE_CHOICES, default='merchant', max_length=20)
    merchant_id = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True, unique=True)
    username = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    has_pos = models.BooleanField(default=False)
    objects = CustomAccountManager()
    force_password_change_on_first_time = models.BooleanField(default=True)
    # TODO: remove null and blank fields
    date = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'password']

    def __str__(self):
        return f'name: {self.name} - phone: {self.username}'
