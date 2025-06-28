@echo off
echo.
echo ================================================================================
echo                    🎬 DJANGO FILM STREAMING SERVER
echo ================================================================================
echo.

cd /d "%~dp0"

echo 🔧 Checking server requirements...
python manage.py check --deploy > nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Running basic check instead...
    python manage.py check
)

echo.
echo 🗄️ Applying any pending migrations...
python manage.py migrate --run-syncdb > nul 2>&1

echo.
echo 📁 Collecting static files...
python manage.py collectstatic --noinput > nul 2>&1

echo.
echo ================================================================================
echo                        🚀 STARTING SERVER
echo ================================================================================
echo.
echo 🌐 Server will be available at:
echo    👉 http://localhost:8000/
echo    👉 http://127.0.0.1:8000/
echo.
echo 📝 Admin credentials:
echo    Username: admin
echo    Password: admin123
echo.
echo 🎬 Available pages:
echo    🏠 Homepage: http://localhost:8000/
echo    🎥 Films: http://localhost:8000/films/
echo    📊 Management: http://localhost:8000/films/management/
echo    👑 Admin: http://localhost:8000/admin/
echo.
echo Press Ctrl+C to stop the server
echo ================================================================================

python manage.py runserver 0.0.0.0:8000
