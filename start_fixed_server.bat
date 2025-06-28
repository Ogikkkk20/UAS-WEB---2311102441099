@echo off
echo ==================================================
echo        FIXED FILM CRUD - READY TO TEST!
echo ==================================================
echo.

cd /d "%~dp0"

echo [INFO] URL Configuration Fixed:
echo   - Removed namespace conflict
echo   - Fixed CKEditor issues  
echo   - Updated template references
echo   - Form validation improved
echo.

echo [TESTING] Starting Django development server...
echo.
echo ACCESS POINTS:
echo   🏠 Homepage: http://localhost:8000/
echo   📊 Dashboard: http://localhost:8000/dashboard/
echo   🎬 Film Management: http://localhost:8000/films/management/
echo   ➕ Add Film: http://localhost:8000/films/management/create/
echo   👥 User Management: http://localhost:8000/users/management/
echo.
echo LOGIN CREDENTIALS:
echo   Username: admin
echo   Password: admin123
echo.
echo ==================================================
echo Starting server on http://localhost:8000/
echo Press Ctrl+C to stop
echo ==================================================
echo.

python manage.py runserver 8000
