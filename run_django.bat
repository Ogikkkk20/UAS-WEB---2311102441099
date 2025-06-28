@echo off
cd /d "C:\Users\nazri\OneDrive\Desktop\joki uas\2311102441099-Ogi-Febrian-Saputra"
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.
echo Testing PyMySQL import...
python -c "import pymysql; print('✅ PyMySQL OK!')"
echo.
echo Testing Django configuration...
python manage.py check
echo.
echo Running Django migrations...
python manage.py migrate
echo.
echo Creating superuser (if needed)...
echo Username: admin
echo Password: admin123
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
echo.
echo Starting Django server...
echo Open browser at: http://127.0.0.1:8000
echo Admin panel at: http://127.0.0.1:8000/admin/
echo Database view at: http://127.0.0.1:8000/database/
echo.
python manage.py runserver
pause
