@echo off
echo ==================================================
echo        DJANGO FILM CRUD - NAMESPACE FIXED!
echo ==================================================
echo.

cd /d "%~dp0"

echo ✅ ISSUES RESOLVED:
echo   - URL namespace configuration fixed
echo   - CKEditor replaced with textarea
echo   - Form validation working
echo   - Template references updated
echo.

echo 🎯 ACCESS POINTS:
echo   🏠 Homepage: http://localhost:8000/
echo   📊 Dashboard: http://localhost:8000/dashboard/
echo   🎬 Film Management: http://localhost:8000/films/management/
echo   ➕ Add Film: http://localhost:8000/films/management/create/
echo   👥 User Management: http://localhost:8000/users/management/
echo.

echo 🔐 LOGIN CREDENTIALS:
echo   Username: admin
echo   Password: admin123
echo.

echo ==================================================
echo Starting Django development server...
echo Press Ctrl+C to stop the server
echo ==================================================
echo.

python manage.py runserver 8000
