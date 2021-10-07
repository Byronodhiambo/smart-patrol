from django.db import models
from django.contrib.auth.models import Group



# Create your models here.
# creating the group table in db
class ChatGroup(Group):
    """ extend Group model to add extra info"""
    description = models.TextField(blank=True, help_text="description of the group")
    mute_notifications = models.BooleanField(default=False, help_text="disable notification if true")
    icon = models.ImageField(help_text="Group icon", blank=True, upload_to="chartgroup")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('chat:room', args=[str(self.id)])


# creating the report table in the db
class Report(models.Model):
    """docstring for Report."""
    security_guard = models.CharField(max_length=100)
    assigned_area = models.CharField(max_length=100)
    date_reported = models.DateTimeField(auto_now_add=True)
    location  = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
