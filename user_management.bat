@echo off
title Django User Management Setup
color 0A

echo.
echo ==========================================
echo 🚀 DJANGO USER MANAGEMENT SETUP
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

echo ⚙️ Running Django check...
python manage.py check
if errorlevel 1 (
    echo ❌ Django check failed
    pause
    exit /b 1
)
echo.

echo 🗄️ Running migrations...
python manage.py migrate
echo.

echo 👤 Setting up admin user...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
echo.

echo 📊 Current user count...
python manage.py shell -c "from django.contrib.auth.models import User; print(f'Current users: {User.objects.count()}')"
echo.

:MENU
echo ==========================================
echo 📋 PILIHAN MENU:
echo ==========================================
echo 1. Buat dummy users (15 users)
echo 2. Buat dummy films (10 films)
echo 3. Buat dummy users + films
echo 4. Lihat database users
echo 5. Lihat database films
echo 6. Jalankan Django server
echo 7. Keluar
echo ==========================================
echo.

set /p choice="Pilih opsi (1-7): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Membuat 15 dummy users...
    python simple_dummy_users.py
    echo.
    goto MENU
)

if "%choice%"=="2" (
    echo.
    echo 🎬 Membuat dummy films...
    python create_dummy_films.py
    echo.
    goto MENU
)

if "%choice%"=="3" (
    echo.
    echo 🚀 Membuat dummy users dan films...
    python simple_dummy_users.py
    echo.
    python create_dummy_films.py
    echo.
    goto MENU
)

if "%choice%"=="4" (
    echo.
    echo 📊 DATABASE USERS:
    echo ==========================================
    python manage.py shell -c "
from django.contrib.auth.models import User
print('Total users:', User.objects.count())
print('Admins:', User.objects.filter(is_superuser=True).count())
print('Staff:', User.objects.filter(is_staff=True, is_superuser=False).count())
print('Regular:', User.objects.filter(is_staff=False, is_superuser=False).count())
print('Active:', User.objects.filter(is_active=True).count())
print()
print('User List:')
print('-' * 80)
for user in User.objects.all()[:20]:
    status = 'Admin' if user.is_superuser else ('Staff' if user.is_staff else 'User')
    active = 'Active' if user.is_active else 'Inactive'
    print(f'{user.id:>3} | {user.username:<15} | {user.first_name} {user.last_name:<20} | {status:<6} | {active}')
"
    echo.
    echo Tekan Enter untuk kembali ke menu...
    pause >nul
    goto MENU
)

if "%choice%"=="4" (
    echo.
    echo 🚀 Starting Django server...
    echo.
    echo 🔗 Available URLs:
    echo   • Home: http://127.0.0.1:8000
    echo   • User Management: http://127.0.0.1:8000/users/
    echo   • Admin Panel: http://127.0.0.1:8000/admin/
    echo   • Database View: http://127.0.0.1:8000/database/
    echo   • Login: http://127.0.0.1:8000/login
    echo.
    echo 🔑 Login Credentials:
    echo   • Admin: admin / admin123
    echo   • Dummy Users: [username] / password123
    echo.
    echo Press Ctrl+C to stop the server
    echo.
    python manage.py runserver
    goto END
)

if "%choice%"=="5" (
    goto END
)

echo Invalid choice. Please try again.
echo.
goto MENU

:END
echo.
echo 👋 Goodbye!
pause
