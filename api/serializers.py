"""
MindBloom Serializers
Translates between Python model objects and JSON.
Also validates incoming data from the React frontend.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Mood, JournalEntry, EmergencyContact


# ─────────────────────────────────────────────────────
# REGISTER SERIALIZER
# Used for user signup. Password is write_only — it's
# accepted as input but never returned in responses.
# ─────────────────────────────────────────────────────
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model  = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # create_user automatically hashes the password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user


# ─────────────────────────────────────────────────────
# USER SERIALIZER
# Returns safe user info (no password ever).
# Used after login/signup and in /auth/me/
# ─────────────────────────────────────────────────────
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['id', 'username', 'email']


# ─────────────────────────────────────────────────────
# MOOD SERIALIZER
# 'user' field is excluded — we assign it from
# request.user in the view (logged-in user only).
# ─────────────────────────────────────────────────────
class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Mood
        fields = ['id', 'mood', 'note', 'date']


# ─────────────────────────────────────────────────────
# JOURNAL ENTRY SERIALIZER
# ─────────────────────────────────────────────────────
class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model  = JournalEntry
        fields = ['id', 'title', 'content', 'created_at']


# ─────────────────────────────────────────────────────
# EMERGENCY CONTACT SERIALIZER
# ─────────────────────────────────────────────────────
class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model  = EmergencyContact
        fields = ['id', 'name', 'phone', 'email']
