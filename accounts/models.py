from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User Model for Hospital Website
    Uses Django's AbstractUser
    """

    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # role flags
    is_admin = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=True)

    def __str__(self):
        return self.username