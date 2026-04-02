/**
 * MindBloom API Helper
 * Drop this file into your React project's src/ folder.
 * Import any function to replace localStorage with real API calls.
 *
 * Usage example:
 *   import { login, getMoods, logMood } from './api';
 *   const user = await login({ username: 'alice', password: 'pass123' });
 */

const BASE_URL = 'http://localhost:8000/api';

// ─────────────────────────────────────────────────────
// CSRF TOKEN HELPER
// Django requires this token for POST/DELETE requests.
// It's automatically set as a cookie by Django.
// ─────────────────────────────────────────────────────
function getCsrfToken() {
  const name = 'csrftoken';
  for (const cookie of document.cookie.split(';')) {
    const c = cookie.trim();
    if (c.startsWith(name + '=')) return c.substring(name.length + 1);
  }
  return '';
}

// ─────────────────────────────────────────────────────
// CENTRAL FETCH FUNCTION
// All API calls go through here.
// credentials: 'include' sends the session cookie automatically.
// ─────────────────────────────────────────────────────
async function apiCall(endpoint, method = 'GET', body = null) {
  const options = {
    method,
    credentials: 'include',   // IMPORTANT: send cookies with every request
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken(),
    },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, options);

  // 204 No Content (e.g. after DELETE) — return null
  if (response.status === 204) return null;

  const data = await response.json();

  // Attach status code so callers can check it if needed
  data._status = response.status;
  return data;
}

// ═════════════════════════════════════════════════════
// AUTH
// ═════════════════════════════════════════════════════

/** Sign up a new user. Returns user object or error. */
export const register = (data) => apiCall('/auth/register/', 'POST', data);

/** Log in with username + password. Returns user object or error. */
export const login = (data) => apiCall('/auth/login/', 'POST', data);

/** Log out. Clears the session. */
export const logout = () => apiCall('/auth/logout/', 'POST');

/**
 * Get current logged-in user.
 * Call this on app load — if it returns a user, they're logged in.
 * If it returns 403, show the login screen.
 */
export const getMe = () => apiCall('/auth/me/');

// ═════════════════════════════════════════════════════
// MOOD
// ═════════════════════════════════════════════════════

/** Get full mood history for the logged-in user. */
export const getMoods = () => apiCall('/moods/');

/**
 * Log today's mood.
 * data = { mood: 'happy', note: 'optional note' }
 * Returns error if mood already logged today.
 */
export const logMood = (data) => apiCall('/moods/', 'POST', data);

/**
 * Check if user has already logged a mood today.
 * Returns mood object if yes, { logged: false } if no.
 */
export const getTodayMood = () => apiCall('/moods/today/');

// ═════════════════════════════════════════════════════
// JOURNAL
// ═════════════════════════════════════════════════════

/** Get all journal entries for the logged-in user. */
export const getJournal = () => apiCall('/journal/');

/**
 * Create a new journal entry.
 * data = { title: 'My Day', content: 'Today was...' }
 */
export const createJournal = (data) => apiCall('/journal/', 'POST', data);

/** Delete a journal entry by its ID. */
export const deleteJournal = (id) => apiCall(`/journal/${id}/`, 'DELETE');

// ═════════════════════════════════════════════════════
// EMERGENCY CONTACT
// ═════════════════════════════════════════════════════

/** Get the user's saved emergency contact. */
export const getContact = () => apiCall('/emergency-contact/');

/**
 * Save or update emergency contact.
 * data = { name: 'Mom', phone: '+91 9876543210', email: 'mom@email.com' }
 */
export const saveContact = (data) => apiCall('/emergency-contact/', 'POST', data);
