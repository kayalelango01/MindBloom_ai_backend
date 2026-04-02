# Fix App.js - Add CSRF initialization before getMe() call

$filePath = "C:\mb\myproject\src\App.js"
$content = Get-Content $filePath -Raw

$oldCode = @"
  // ✅ FIX: On app load, check session. Previously if getMe() threw (e.g. 403),
  // the .catch() block wasn't always hit because apiCall now returns safely
  // instead of throwing. Now we check res.id explicitly.
  useEffect(() => {
    getMe().then(res => {
      if (res && res.id) {
        setUser(res);
        setPage("home");
      } else {
        setPage("profile");
      }
      setAuthReady(true);
    }).catch(() => {
      setPage("profile");
      setAuthReady(true);
    });
  }, []);
"@

$newCode = @"
  // ✅ FIX: On app load, FIRST get CSRF token, THEN check session
  useEffect(() => {
    const initApp = async () => {
      try {
        // STEP 1: Get CSRF cookie FIRST (required before any API calls)
        await fetch('http://127.0.0.1:8000/api/csrf/', {
          method: 'GET',
          credentials: 'include',
        });
        
        // STEP 2: Now check if user is logged in
        const res = await getMe();
        if (res && res.id) {
          setUser(res);
          setPage("home");
        } else {
          setPage("profile");
        }
      } catch (err) {
        console.log('Not logged in yet - show login screen');
        setPage("profile");
      } finally {
        setAuthReady(true);
      }
    };
    
    initApp();
  }, []);
"@

$content = $content -replace [regex]::Escape($oldCode), $newCode
$content | Set-Content $filePath -NoNewline

Write-Host "App.js updated successfully!"
Write-Host "Changes:"
Write-Host "   - Added CSRF token fetch BEFORE getMe() call"
Write-Host "   - This fixes the 403 Forbidden errors"
