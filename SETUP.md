# MindBloom Backend — VS Code Setup Guide

## STEP 1: Open in VS Code
Open the `mindbloom-backend` folder in VS Code.
Then open the integrated terminal: View → Terminal

---

## STEP 2: Create virtual environment
```
python -m venv venv
```

---

## STEP 3: Activate it (run this EVERY TIME you open the project)
**Windows:**
```
venv\Scripts\activate
```
**Mac / Linux:**
```
source venv/bin/activate
```
You'll see `(venv)` in your terminal prompt when it's active.

---

## STEP 4: Install all packages
```
pip install -r requirements.txt
```

---

## STEP 5: Create the database tables
```
python manage.py makemigrations
python manage.py migrate
```

---

## STEP 6: Create your admin account (one time only)
```
python manage.py createsuperuser
```
Pick any username, email, and password.

---

## STEP 7: Start the server
```
python manage.py runserver
```
Your API is now live at: http://localhost:8000/
Django Admin panel: http://localhost:8000/admin/

---

## API ENDPOINTS QUICK REFERENCE

| Method | URL                          | What it does               |
|--------|------------------------------|----------------------------|
| POST   | /api/auth/register/          | Sign up new user           |
| POST   | /api/auth/login/             | Login                      |
| POST   | /api/auth/logout/            | Logout                     |
| GET    | /api/auth/me/                | Get current user info      |
| GET    | /api/moods/                  | Get mood history           |
| POST   | /api/moods/                  | Log today's mood           |
| GET    | /api/moods/today/            | Check if mood logged today |
| GET    | /api/journal/                | Get all journal entries    |
| POST   | /api/journal/                | Create new entry           |
| DELETE | /api/journal/<id>/           | Delete entry by ID         |
| GET    | /api/emergency-contact/      | Get emergency contact      |
| POST   | /api/emergency-contact/      | Save emergency contact     |

---

## REACT INTEGRATION
Copy `api.js` from this folder into your React project's `src/` folder.
Then import what you need:
```js
import { login, getMoods, logMood } from './api';
```

---

## COMMON ERRORS

**"No module named django"**
→ You forgot to activate venv. Run Step 3 again.

**CORS error in browser**
→ Make sure your React app runs on port 3000.
→ Check that corsheaders is FIRST in MIDDLEWARE in settings.py.

**"No such table"**
→ Run: python manage.py migrate

**403 Forbidden on API calls**
→ User is not logged in. Call /api/auth/login/ first.
