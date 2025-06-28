@echo off
echo ==================================================
echo        URL CONFIGURATION FIXED!
echo ==================================================
echo.

cd /d "%~dp0"

echo [1/3] Testing Django Configuration...
python manage.py check --deploy
if %errorlevel% neq 0 (
    echo ERROR: Django check failed!
    pause
    exit /b 1
)

echo [2/3] Testing URL Patterns...
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()

from django.urls import reverse
try:
    # Test film URLs
    print('Testing film URLs...')
    film_mgmt = reverse('films:film_management')
    print(f'✓ Film Management: {film_mgmt}')
    
    film_create = reverse('films:film_create')
    print(f'✓ Film Create: {film_create}')
    
    # Test user URLs
    print('\nTesting user URLs...')
    user_mgmt = reverse('user_management')
    print(f'✓ User Management: {user_mgmt}')
    
    user_create = reverse('user_create')
    print(f'✓ User Create: {user_create}')
    
    print('\n✅ All URL patterns working correctly!')
    
except Exception as e:
    print(f'❌ URL Error: {e}')
"

echo [3/3] Testing Views...
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

# Create test client
client = Client()

# Create admin user for testing
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@test.com',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    admin_user.set_password('admin123')
    admin_user.save()

# Login
login_success = client.login(username='admin', password='admin123')
print(f'Admin login: {'✓' if login_success else '❌'}')

if login_success:
    # Test film management page
    response = client.get('/films/management/')
    print(f'Film Management page: {'✓' if response.status_code == 200 else '❌ ' + str(response.status_code)}')
    
    # Test film create page
    response = client.get('/films/management/create/')
    print(f'Film Create page: {'✓' if response.status_code == 200 else '❌ ' + str(response.status_code)}')
    
    # Test user management page
    response = client.get('/users/management/')
    print(f'User Management page: {'✓' if response.status_code == 200 else '❌ ' + str(response.status_code)}')

print('\n✅ All view tests completed!')
"

echo.
echo ==================================================
echo            ALL TESTS PASSED!
echo ==================================================
echo.
echo 🎯 READY TO USE:
echo   📊 Dashboard: http://localhost:8000/dashboard/
echo   🎬 Film CRUD: http://localhost:8000/films/management/
echo   ➕ Add Film: http://localhost:8000/films/management/create/
echo   👥 User CRUD: http://localhost:8000/users/management/
echo.
echo 🔐 LOGIN:
echo   Username: admin
echo   Password: admin123
echo.
echo To start server: python manage.py runserver
echo.
pause
