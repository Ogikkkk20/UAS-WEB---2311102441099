# Django MySQL Setup Script
# Run this script in PowerShell

Write-Host "🚀 Django MySQL Setup Script" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green

# Set location
Set-Location "C:\Users\nazri\OneDrive\Desktop\joki uas\2311102441099-Ogi-Febrian-Saputra"

# Check if virtual environment exists
if (Test-Path "venv") {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
}
else {
    Write-Host "❌ Virtual environment not found" -ForegroundColor Red
    Write-Host "Creating new virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install packages
Write-Host "📦 Installing packages..." -ForegroundColor Yellow
pip install Django==5.1.7 Pillow==10.4.0 pymysql

# Test imports
Write-Host "🧪 Testing imports..." -ForegroundColor Yellow
python -c "import django; print('✅ Django OK')"
python -c "import pymysql; print('✅ PyMySQL OK')"
python -c "import PIL; print('✅ Pillow OK')"

# Check Django configuration
Write-Host "⚙️  Checking Django configuration..." -ForegroundColor Yellow
python manage.py check

# Run migrations
Write-Host "🗄️  Running migrations..." -ForegroundColor Yellow
python manage.py migrate

# Create superuser if not exists
Write-Host "👤 Setting up admin user..." -ForegroundColor Yellow
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Admin user created: admin/admin123')
else:
    print('✅ Admin user already exists: admin/admin123')
"

Write-Host ""
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host "==================" -ForegroundColor Green
Write-Host "📋 Available URLs:" -ForegroundColor Cyan
Write-Host "  • Home: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "  • Admin: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host "  • Database: http://127.0.0.1:8000/database/" -ForegroundColor White
Write-Host "  • Login: http://127.0.0.1:8000/login" -ForegroundColor White
Write-Host "  • Register: http://127.0.0.1:8000/registrasi" -ForegroundColor White
Write-Host ""
Write-Host "🔑 Admin Credentials:" -ForegroundColor Cyan
Write-Host "  • Username: admin" -ForegroundColor White
Write-Host "  • Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Starting Django server..." -ForegroundColor Yellow

# Start server
python manage.py runserver
