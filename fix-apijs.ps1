$filePath = "C:\mb\myproject\src\api.js"
$content = Get-Content $filePath -Raw

$oldCode = @"
// ─────────────────────────────────────────────────────
// CSRF TOKEN HELPER
// Django requires this token for POST/DELETE requests.
// It's automatically set as a cookie by Django when you
// call GET /api/csrf/ first.
// ─────────────────────────────────────────────────────
function getCsrfToken() {
  const name = 'csrftoken';
  for (const cookie of document.cookie.split(';')) {
    const c = cookie.trim();
    if (c.startsWith(name + '=')) return c.substring(name.length + 1);
  }
  return '';
}

// ✅ FIX: Returns a promise — callers must await this before reading the cookie.
async function ensureCSRF() {
  // Only fetch if cookie isn't already present
  if (getCsrfToken()) return;
  await fetch(`${BASE_URL}/csrf/`, {
    method: 'GET',
    credentials: 'include',
  });
}
"@

$newCode = @"
// ─────────────────────────────────────────────────────
// CSRF TOKEN HELPER
// Django requires this token for POST/DELETE requests.
// Stores token in both cookie and localStorage for reliability.
// ─────────────────────────────────────────────────────
function getCsrfToken() {
  // Try to get from localStorage first (more reliable)
  let token = localStorage.getItem('mb_csrf_token');
  if (token) return token;
  
  // Fallback to cookie
  const name = 'csrftoken';
  for (const cookie of document.cookie.split(';')) {
    const c = cookie.trim();
    if (c.startsWith(name + '=')) {
      token = c.substring(name.length + 1);
      localStorage.setItem('mb_csrf_token', token);
      return token;
    }
  }
  return '';
}

// ✅ FIX: Fetches CSRF token and stores it in localStorage for reliability.
async function ensureCSRF() {
  // Only fetch if we don't already have a token
  if (getCsrfToken()) return;
  
  const response = await fetch(`${BASE_URL}/csrf/`, {
    method: 'GET',
    credentials: 'include',
  });
  
  const data = await response.json();
  // Store token from response in localStorage
  if (data.csrfToken) {
    localStorage.setItem('mb_csrf_token', data.csrfToken);
  }
}
"@

$content = $content -replace [regex]::Escape($oldCode), $newCode
$content | Set-Content $filePath -NoNewline

Write-Host "api.js updated successfully!"
Write-Host "Now uses localStorage instead of cookies for CSRF token"
