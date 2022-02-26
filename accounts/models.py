from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Profile(models.Model):
    """docstring for Profile."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(help_text="profile pic", blank=True, upload_to="users")
    phone_number = models.IntegerField()
    estate = models.CharField(max_length=20)
    assigned_area = models.CharField(max_length=20)
    postal_address = models.CharField(max_length=20, default=100)


    def __str__(self):
        return self.assigned_area
