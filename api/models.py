"""
MindBloom Database Models
"""

from django.db import models
from django.contrib.auth.models import User


class Mood(models.Model):
    # ✅ FIX: choices now match exactly what React sends (capitalised)
    MOOD_CHOICES = [
        ('Happy',    'Happy'),
        ('Sad',      'Sad'),
        ('Anxious',  'Anxious'),
        ('Calm',     'Calm'),
        ('Neutral',  'Neutral'),
        ('Stressed', 'Stressed'),
        # kept extras in case old data exists
        ('Angry',    'Angry'),
        ('Excited',  'Excited'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moods')
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    note = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} — {self.mood} on {self.date}"


class JournalEntry(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')
    title      = models.CharField(max_length=200)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} — {self.title}"


class EmergencyContact(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='emergency_contact')
    name  = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s contact: {self.name}"
