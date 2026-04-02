"""
Register models with Django Admin.
After this, you can view/edit all data at http://localhost:8000/admin/
"""

from django.contrib import admin
from .models import Mood, JournalEntry, EmergencyContact


@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display  = ['user', 'mood', 'date', 'note']
    list_filter   = ['mood', 'date']
    search_fields = ['user__username']


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display  = ['user', 'title', 'created_at']
    search_fields = ['user__username', 'title']


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display  = ['user', 'name', 'phone', 'email']
    search_fields = ['user__username', 'name']
