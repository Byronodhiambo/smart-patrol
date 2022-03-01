from django.contrib import admin
from .models import ChatGroup, Report

# Register your models here.
class ChatGroupAdmin(admin.ModelAdmin):
    """ enable Chart Group admin """
    list_display = ('id', 'name', 'description', 'icon', 'mute_notifications', 'date_created', 'date_modified')
    list_filter = ('id', 'name', 'description', 'icon', 'mute_notifications', 'date_created', 'date_modified')
    list_display_links = ('name',)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'security_guard', 'assigned_area', 'date_reported', 'location', 'category', 'description')
    list_filter = ('id', 'security_guard', 'assigned_area', 'date_reported', 'location', 'category', 'description')
    list_display_links = ('security_guard',)

admin.site.register(ChatGroup, ChatGroupAdmin)

admin.site.register(Report, ReportAdmin)
