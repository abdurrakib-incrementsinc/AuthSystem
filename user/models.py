import uuid

import pyotp
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from authsystem.models import BaseModel
from django.db.models.signals import post_save
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(_('ID'), primary_key=True, default=uuid.uuid4)
    email = models.EmailField(_('Email'), max_length=150, unique=True, null=True, blank=True)
    username = models.CharField(_('Username'), max_length=150, unique=True)
    date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('Last Login'), auto_now=True)
    is_staff = models.BooleanField(
        _('Staff Status'),
        default=False,
        help_text="Designate if the user has staff status"
    )
    is_active = models.BooleanField(
        _('Active Status'),
        default=False,
        help_text="Designate if the user has active status",
    )
    is_superuser = models.BooleanField(
        _('Superuser Status'),
        default=False,
        help_text='Designate if the user has superuser status',
    )
    is_manager = models.BooleanField(
        _('Manager Status'),
        default=False,
        help_text='Designate if the user has manager status',
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class UserInformation(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_information')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=350, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_images', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}-information"


class OTPModel(BaseModel):
    """
    Model to handle user OTP
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_otp")
    key = models.TextField(unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP - {self.user.username} - {self.user.email}"


@receiver(post_save, sender=User)
def create_instance(sender, instance, created, **kwargs):
    if created:
        OTPModel.objects.create(user=instance, key=pyotp.random_base32())


