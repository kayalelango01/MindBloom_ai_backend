# MindBloom Frontend Integration Guide

## ⚠️ CRITICAL: Fix Your Frontend Code

The 403 errors happen because your React frontend is NOT calling the CSRF endpoint first. Here's how to fix it:

---

## STEP 1: Update Your API Calls in Frontend

In your React app, you need to call `/api/csrf/` FIRST before any authentication or data operations.

### Example Fix in Your React Component:

```javascript
// In your App.jsx or main component
import { useEffect, useState } from 'react';
import { register, login, getMe, logMood, getMoods } from './api'; // adjust path

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // STEP 1: Get CSRF token FIRST
    const initApp = async () => {
      try {
        // Call CSRF endpoint to set the cookie
        await fetch('http://localhost:8000/api/csrf/', {
          method: 'GET',
          credentials: 'include',
        });
        
        // STEP 2: Now check if user is already logged in
        const userData = await getMe();
        if (userData && userData.username) {
          setUser(userData);
        }
      } catch (error) {
        console.log('Not logged in yet - show login screen');
      } finally {
        setLoading(false);
      }
    };

    initApp();
  }, []);

  // Your registration function
  const handleRegister = async (username, password, email) => {
    try {
      // CSRF was already called in useEffect, so this will work
      const result = await register({ username, password, email });
      if (result.username) {
        setUser(result);
      } else {
        console.error('Registration failed:', result);
      }
    } catch (error) {
      console.error('Registration error:', error);
    }
  };

  // Your login function
  const handleLogin = async (username, password) => {
    try {
      const result = await login({ username, password });
      if (result.username) {
        setUser(result);
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  // Your mood logging function
  const handleSaveMood = async (mood, note) => {
    try {
      const result = await logMood({ mood, note });
      console.log('Mood saved:', result);
    } catch (error) {
      console.error('Failed to save mood:', error);
    }
  };

  if (loading) return <div>Loading...</div>;
  
  return (
    // Your app JSX here
  );
}
```

---

## STEP 2: Verify Your API Helper File

Make sure your `api.js` file has these settings:

```javascript
async function apiCall(endpoint, method = 'GET', body = null) {
  const options = {
    method,
    credentials: 'include',   // ← MUST include cookies
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken(),  // ← MUST send CSRF token
    },
  };
  // ... rest of the code
}
```

---

## STEP 3: Test Order of Operations

Your frontend MUST follow this sequence:

1. **FIRST**: Call `GET /api/csrf/` → Sets CSRF cookie in browser
2. **SECOND**: Call `/api/auth/register/` or `/api/auth/login/` → Creates session
3. **THIRD**: All other API calls (`/api/moods/`, `/api/journal/`, etc.)

---

## COMMON MISTAKES TO AVOID

❌ **DON'T** skip the CSRF call
❌ **DON'T** use `credentials: 'omit'` or `'same-origin'` — must be `'include'`
❌ **DON'T** forget to send `X-CSRFToken` header in POST requests
❌ **DON'T** try to call mood/journal endpoints before logging in

✅ **DO** call `/api/csrf/` on app initialization
✅ **DO** use `credentials: 'include'` in ALL fetch calls
✅ **DO** check if user is authenticated before showing protected pages

---

## QUICK DEBUG CHECKLIST

If you still see 403 errors:

1. Open browser DevTools → Application → Cookies
   - Check if `csrftoken` cookie exists after calling `/api/csrf/`
   
2. Check Network tab for your API calls:
   - Request Headers should include: `X-CSRFToken: <token_value>`
   - Request Headers should include: `Cookie: csrftoken=...; sessionid=...`
   
3. Verify your frontend is calling `/api/csrf/` BEFORE any POST requests

4. Check browser console for CORS errors:
   - If you see CORS errors, make sure your React dev server is running on port 3000-3015
   
---

## EXAMPLE REACT COMPONENT STRUCTURE

```
src/
├── App.jsx              ← Main app with CSRF initialization
├── api.js               ← API helper (copy from backend)
├── components/
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── MoodTracker.jsx
│   └── Journal.jsx
```

In `App.jsx`:
```javascript
useEffect(() => {
  // Initialize CSRF and auth check
  fetch('http://localhost:8000/api/csrf/', { credentials: 'include' })
    .then(() => getMe())
    .then(setUser)
    .catch(() => setShowLogin(true));
}, []);
```

---

## TESTING THE FIX

After making these changes:

1. Clear your browser cache and cookies
2. Restart your React dev server
3. Make sure Django backend is running on http://localhost:8000
4. Open your app in browser
5. Check Network tab - you should see:
   - First request: `/api/csrf/` → Status 200
   - Second request: `/api/auth/register/` or `/api/auth/login/` → Status 200/201
   - Subsequent requests: `/api/moods/`, etc. → Status 200/201

---

## STILL HAVING ISSUES?

Run this test in your browser console:

```javascript
// Test 1: Get CSRF cookie
fetch('http://localhost:8000/api/csrf/', { credentials: 'include' })
  .then(r => r.json())
  .then(console.log);

// Wait 1 second, then test 2: Register
setTimeout(() => {
  fetch('http://localhost:8000/api/auth/register/', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': document.cookie.split('csrftoken=')[1]?.split(';')[0]
    },
    body: JSON.stringify({
      username: 'testuser',
      password: 'testpass123',
      email: 'test@example.com'
    })
  })
  .then(r => r.json())
  .then(console.log);
}, 1000);
```

If this works, your issue is in your React code structure.
If this fails, there's a backend configuration issue.
