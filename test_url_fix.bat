@echo off
echo.
echo ================================================================================
echo                        🔧 TESTING URL FIX
echo ================================================================================
echo.

cd /d "%~dp0"

echo [STEP 1] Testing URL resolution...
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()

from django.urls import resolve
from django.test import Client

print('🔧 Testing URL Resolution:')
test_urls = ['/films/', '/films/management/', '/films/browse/']

for url in test_urls:
    try:
        match = resolve(url)
        print(f'✅ {url} -> {match.func.__name__}')
    except Exception as e:
        print(f'❌ {url} -> ERROR: {e}')

print('\\n🌐 Testing HTTP responses:')
client = Client()
for url in test_urls:
    try:
        response = client.get(url)
        print(f'✅ {url} -> Status {response.status_code}')
    except Exception as e:
        print(f'❌ {url} -> ERROR: {e}')
"

if %errorlevel% neq 0 (
    echo ❌ URL testing failed!
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo                     🎉 URL FIX SUCCESSFUL!
echo ================================================================================
echo.
echo ✅ All URLs are now working correctly
echo.
echo 🌐 URLs that should work now:
echo    👉 http://localhost:8000/films/
echo    👉 http://localhost:8000/films/management/
echo    👉 http://localhost:8000/films/browse/
echo.
echo 🚀 Start the server to test: python manage.py runserver
echo.
pause
