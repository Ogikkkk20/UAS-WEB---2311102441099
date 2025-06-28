@echo off
title Film Management System
color 0A

echo.
echo ==========================================
echo 🎬 FILM MANAGEMENT SYSTEM
echo ==========================================
echo.

cd /d "C:\Users\nazri\OneDrive\Desktop\joki uas\2311102441099-Ogi-Febrian-Saputra"

echo 📁 Current directory: %CD%
echo.

echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment activated
echo.

echo 🧪 Testing imports...
python -c "import django; print('✅ Django OK')"
python -c "import pymysql; print('✅ PyMySQL OK')"
echo.

echo ⚙️ Running Django migrations...
python manage.py makemigrations
python manage.py migrate
echo.

echo 👤 Setting up admin user...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
echo.

:MENU
echo ==========================================
echo 📋 MENU OPTIONS:
echo ==========================================
echo 1. Create dummy users (15 users)
echo 2. Create dummy films (10 films)
echo 3. Create both users and films
echo 4. View database summary
echo 5. Start Django server
echo 6. Open film management
echo 7. Exit
echo ==========================================
echo.

set /p choice="Choose option (1-7): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Creating 15 dummy users...
    python simple_dummy_users.py
    echo.
    goto MENU
)

if "%choice%"=="2" (
    echo.
    echo 🎬 Creating dummy films...
    python create_dummy_films.py
    echo.
    goto MENU
)

if "%choice%"=="3" (
    echo.
    echo 🚀 Creating dummy users and films...
    python simple_dummy_users.py
    echo.
    python create_dummy_films.py
    echo.
    goto MENU
)

if "%choice%"=="4" (
    echo.
    echo 📊 DATABASE SUMMARY:
    echo ==========================================
    python manage.py shell -c "
from django.contrib.auth.models import User
from films.models import Film, Genre
print('=== USERS ===')
print(f'Total users: {User.objects.count()}')
print(f'Admin users: {User.objects.filter(is_superuser=True).count()}')
print(f'Staff users: {User.objects.filter(is_staff=True, is_superuser=False).count()}')
print(f'Regular users: {User.objects.filter(is_staff=False, is_superuser=False).count()}')
print()
print('=== FILMS ===')
print(f'Total films: {Film.objects.count()}')
print(f'Published films: {Film.objects.filter(status=\"published\").count()}')
print(f'Featured films: {Film.objects.filter(featured=True).count()}')
print(f'Total genres: {Genre.objects.count()}')
print()
print('Recent Films:')
for film in Film.objects.all()[:5]:
    print(f'- {film.title} ({film.director}) - {film.get_status_display()}')
"
    echo.
    echo Press Enter to return to menu...
    pause >nul
    goto MENU
)

if "%choice%"=="5" (
    echo.
    echo 🚀 Starting Django server...
    echo.
    echo 🔗 Available URLs:
    echo   • Film List: http://127.0.0.1:8000/
    echo   • Film Management: http://127.0.0.1:8000/films/management/
    echo   • User Management: http://127.0.0.1:8000/users/
    echo   • Admin Panel: http://127.0.0.1:8000/admin/
    echo   • Database View: http://127.0.0.1:8000/database/
    echo.
    echo 🔑 Login Credentials:
    echo   • Admin: admin / admin123
    echo   • Staff users can access film management
    echo.
    echo Press Ctrl+C to stop the server
    echo.
    python manage.py runserver
    goto END
)

if "%choice%"=="6" (
    echo.
    echo 🌐 Opening film management URLs...
    start http://127.0.0.1:8000/films/management/
    start http://127.0.0.1:8000/users/
    start http://127.0.0.1:8000/admin/
    echo URLs opened in browser. Make sure Django server is running.
    echo.
    goto MENU
)

if "%choice%"=="7" (
    goto END
)

echo Invalid choice. Please try again.
echo.
goto MENU

:END
echo.
echo 👋 Thank you for using Film Management System!
echo.
echo 💡 Quick Tips:
echo   • Run this script anytime to manage your film database
echo   • Use the web interface for better film management experience
echo   • Check the admin panel for advanced configurations
echo.
pause
