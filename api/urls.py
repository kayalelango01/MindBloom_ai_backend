"""
MindBloom API URL Routes
"""

from django.urls import path
from . import views

urlpatterns = [
    # ── AUTH ─────────────────────────────────────────
    path('auth/register/', views.RegisterView.as_view()),
    path('auth/login/',    views.LoginView.as_view()),
    path('auth/logout/',   views.LogoutView.as_view()),
    path('auth/me/',       views.MeView.as_view()),

    # ── MOOD — today/ MUST be before moods/ ──────────
    path('moods/today/', views.TodayMoodView.as_view()),  # ← moved up
    path('moods/',       views.MoodView.as_view()),

    # ── JOURNAL ──────────────────────────────────────
    path('journal/',          views.JournalListView.as_view()),
    path('journal/<int:pk>/', views.JournalDetailView.as_view()),

    # ── EMERGENCY CONTACT ────────────────────────────
    path('emergency-contact/', views.EmergencyContactView.as_view()),
]
