"""
MindBloom API Views — Token Authentication
No CSRF anywhere. Token is stored in localStorage and sent as Authorization header.
"""

import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Mood, JournalEntry, EmergencyContact
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    MoodSerializer,
    JournalEntrySerializer,
    EmergencyContactSerializer,
)


# ═════════════════════════════════════════════════════
# AUTH VIEWS
# ═════════════════════════════════════════════════════

class RegisterView(APIView):
    """POST /api/auth/register/"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            data = UserSerializer(user).data
            data['token'] = token.key
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """POST /api/auth/login/"""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            data = UserSerializer(user).data
            data['token'] = token.key
            return Response(data)

        return Response(
            {'error': 'Invalid username or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    """POST /api/auth/logout/ — deletes the token"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response({'message': 'Logged out successfully'})


class MeView(APIView):
    """GET /api/auth/me/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


# ═════════════════════════════════════════════════════
# MOOD VIEWS
# ═════════════════════════════════════════════════════

class MoodView(APIView):
    """GET /api/moods/ and POST /api/moods/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        moods = Mood.objects.filter(user=request.user).order_by('-date')
        return Response(MoodSerializer(moods, many=True).data)

    def post(self, request):
        today = datetime.date.today()
        if Mood.objects.filter(user=request.user, date=today).exists():
            return Response(
                {'error': 'You have already logged your mood today. Come back tomorrow!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = MoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodayMoodView(APIView):
    """GET /api/moods/today/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = datetime.date.today()
        try:
            mood = Mood.objects.get(user=request.user, date=today)
            return Response(MoodSerializer(mood).data)
        except Mood.DoesNotExist:
            return Response({'logged': False}, status=status.HTTP_404_NOT_FOUND)


# ═════════════════════════════════════════════════════
# JOURNAL VIEWS
# ═════════════════════════════════════════════════════

class JournalListView(APIView):
    """GET /api/journal/ and POST /api/journal/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')
        return Response(JournalEntrySerializer(entries, many=True).data)

    def post(self, request):
        serializer = JournalEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JournalDetailView(APIView):
    """DELETE /api/journal/<id>/"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            entry = JournalEntry.objects.get(pk=pk, user=request.user)
        except JournalEntry.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ═════════════════════════════════════════════════════
# EMERGENCY CONTACT VIEWS
# ═════════════════════════════════════════════════════

class EmergencyContactView(APIView):
    """GET /api/emergency-contact/ and POST /api/emergency-contact/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            contact = EmergencyContact.objects.get(user=request.user)
            return Response(EmergencyContactSerializer(contact).data)
        except EmergencyContact.DoesNotExist:
            return Response({'exists': False}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        contact, created = EmergencyContact.objects.get_or_create(user=request.user)
        serializer = EmergencyContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response(serializer.data, status=code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
