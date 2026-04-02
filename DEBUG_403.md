# 🚨 Quick Debug Steps for 403 Errors

## Your browser is using CACHED old code!

### IMMEDIATE FIX:

#### Option 1: Hard Refresh (Try This First)
1. In your browser, press: **`Ctrl + Shift + R`**
2. Or close the tab and open a new **Incognito/Private window**
3. Go to `http://localhost:3000`

#### Option 2: Clear Cache Completely
1. Press **`Ctrl + Shift + Delete`**
2. Check "Cached images and files"
3. Click "Clear data"
4. Restart browser

#### Option 3: Restart React Dev Server
```bash
# In terminal where npm start is running:
Ctrl + C

# Then restart:
npm start
```

---

## 🔍 After Clearing Cache, Check This:

### Open Browser DevTools (F12) → Console Tab

**Paste this code and press Enter:**
```javascript
// Test 1: Check if CSRF endpoint works
fetch('http://127.0.0.1:8000/api/csrf/', { credentials: 'include' })
  .then(r => r.json())
  .then(d => console.log('✅ CSRF Response:', d))
  .catch(e => console.error('❌ CSRF Error:', e));

// Test 2: Check cookies
setTimeout(() => {
  console.log('🍪 Cookies:', document.cookie);
}, 500);
```

**What you should see:**
```
✅ CSRF Response: {message: "CSRF cookie set", csrfToken: "..."}
🍪 Cookies: csrftoken=...; ...
```

**If you see errors here, the backend isn't reachable.**

---

## ✅ Manual Test Sequence

After clearing cache:

1. **Open Network tab** (F12 → Network)
2. **Refresh page** (Ctrl + Shift + R)
3. **Look for FIRST request:**
   - Should be `/api/csrf/` with status 200
   
4. **Check Request Headers** on that request:
   - Should show proper connection to localhost:8000

5. **Now try registration:**
   - Profile → Sign Up tab
   - Username: `testabc`
   - Password: `test123456`
   - Click Create

6. **Check Network tab again:**
   - Look for `/api/auth/register/`
   - Click on it → Headers tab
   - **Check Request Headers:**
     - `X-CSRFToken`: Should have a value (not empty)
     - `Cookie`: Should include `csrftoken=...`

---

## 🎯 If STILL Getting 403:

### Check Django Terminal Output

In the terminal where Django is running, you should see log entries like:

```
[02/Apr/2026 14:XX:XX] "GET /api/csrf/ HTTP/1.1" 200 54
[02/Apr/2026 14:XX:XX] "POST /api/auth/register/ HTTP/1.1" 201 45
```

**If you DON'T see ANY requests**, your frontend isn't reaching the backend at all.

---

## 🐛 Common Issues

### Issue 1: Wrong Backend URL
Your `api.js` uses `http://127.0.0.1:8000/api` but maybe Django is on different port?

**Check Django terminal** - it should say:
```
Starting development server at http://127.0.0.1:8000/
```

If it says port 8001 or something else, that's the problem!

### Issue 2: CORS Blocking
Open Console (F12) and look for red errors starting with:
```
Access to fetch at 'http://127.0.0.1:8000...' from origin 'http://localhost:3000' has been blocked by CORS policy
```

If you see this, I need to add `localhost:3000` to CORS settings.

### Issue 3: Mixed Content Error
If Console shows:
```
Mixed Content: The page at 'https://...' was loaded over HTTPS, but requested an insecure...
```

This means you're accessing via HTTPS but backend is HTTP. Make sure you use `http://localhost:3000` (not https).

---

## 📋 What to Tell Me

If still broken after trying above, tell me:

1. **What port is React on?** (Check terminal - should say `localhost:3000` or similar)
2. **What port is Django on?** (Should be 8000)
3. **Paste the EXACT error from Console** (F12 → Console tab)
4. **Does `/api/csrf/` work when tested directly?**
   - Open: http://127.0.0.1:8000/api/csrf/
   - Should show JSON: `{"message": "CSRF cookie set", "csrfToken": "..."}`

---

## 🆘 Emergency Fallback

If nothing works, we can temporarily disable CSRF for testing:

I can modify the backend to accept ALL requests without CSRF (development only).
Let me know if you want me to do this as a last resort.
