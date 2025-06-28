@echo off
echo ==================================================
echo        COMPLETE CRUD TEST SCRIPT
echo ==================================================
echo.

cd /d "%~dp0"

echo [1/5] Checking Django project...
python manage.py check --deploy
if %errorlevel% neq 0 (
    echo ERROR: Django check failed!
    pause
    exit /b 1
)

echo [2/5] Applying migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Migration failed!
    pause
    exit /b 1
)

echo [3/5] Collecting static files...
python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo ERROR: Static files collection failed!
    pause
    exit /b 1
)

echo [4/5] Creating test data...
echo Creating superuser (admin/admin123)...
echo from django.contrib.auth.models import User; User.objects.filter(username='admin').delete(); User.objects.create_superuser('admin', 'admin@test.com', 'admin123') | python manage.py shell

echo Creating test users...
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()
from django.contrib.auth.models import User

# Create test users
users_data = [
    {'username': 'john_doe', 'email': 'john@test.com', 'first_name': 'John', 'last_name': 'Doe', 'is_staff': True},
    {'username': 'jane_smith', 'email': 'jane@test.com', 'first_name': 'Jane', 'last_name': 'Smith', 'is_staff': False},
    {'username': 'bob_manager', 'email': 'bob@test.com', 'first_name': 'Bob', 'last_name': 'Manager', 'is_staff': True, 'is_superuser': True},
    {'username': 'alice_user', 'email': 'alice@test.com', 'first_name': 'Alice', 'last_name': 'User', 'is_staff': False}
]

for user_data in users_data:
    username = user_data['username']
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username, user_data['email'], 'password123')
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.is_staff = user_data.get('is_staff', False)
        user.is_superuser = user_data.get('is_superuser', False)
        user.save()
        print(f'Created user: {username}')
    else:
        print(f'User already exists: {username}')
"

echo Creating test films and genres...
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()
from films.models import Genre, Film
from django.contrib.auth.models import User

# Create genres
genres_data = [
    {'name': 'Action', 'description': 'High-energy films with exciting stunts'},
    {'name': 'Drama', 'description': 'Character-driven stories with emotional depth'},
    {'name': 'Comedy', 'description': 'Funny films designed to entertain'},
    {'name': 'Sci-Fi', 'description': 'Science fiction and futuristic themes'},
    {'name': 'Horror', 'description': 'Scary and suspenseful films'},
    {'name': 'Romance', 'description': 'Love stories and romantic themes'}
]

for genre_data in genres_data:
    genre, created = Genre.objects.get_or_create(
        name=genre_data['name'],
        defaults={'description': genre_data['description']}
    )
    if created:
        print(f'Created genre: {genre.name}')

# Create test films
admin_user = User.objects.filter(is_superuser=True).first()
if admin_user:
    films_data = [
        {
            'title': 'The Matrix Reloaded',
            'description': 'Neo continues his fight against the machines in this sci-fi action sequel.',
            'release_year': 2003,
            'duration_minutes': 138,
            'rating': 4.2,
            'genre': 'Sci-Fi'
        },
        {
            'title': 'Inception',
            'description': 'A mind-bending thriller about dreams within dreams.',
            'release_year': 2010,
            'duration_minutes': 148,
            'rating': 4.8,
            'genre': 'Sci-Fi'
        },
        {
            'title': 'The Dark Knight',
            'description': 'Batman faces his greatest challenge in the form of the Joker.',
            'release_year': 2008,
            'duration_minutes': 152,
            'rating': 4.9,
            'genre': 'Action'
        },
        {
            'title': 'Casablanca',
            'description': 'A classic romance set during World War II.',
            'release_year': 1942,
            'duration_minutes': 102,
            'rating': 4.7,
            'genre': 'Romance'
        },
        {
            'title': 'The Shawshank Redemption',
            'description': 'The story of hope and friendship in Shawshank State Penitentiary.',
            'release_year': 1994,
            'duration_minutes': 142,
            'rating': 4.9,
            'genre': 'Drama'
        }
    ]
    
    for film_data in films_data:
        genre = Genre.objects.get(name=film_data['genre'])
        film, created = Film.objects.get_or_create(
            title=film_data['title'],
            defaults={
                'description': film_data['description'],
                'release_year': film_data['release_year'],
                'duration_minutes': film_data['duration_minutes'],
                'rating': film_data['rating'],
                'genre': genre,
                'created_by': admin_user
            }
        )
        if created:
            print(f'Created film: {film.title}')
"

echo [5/5] Starting development server...
echo.
echo ==================================================
echo            TEST DATA CREATED SUCCESSFULLY!
echo ==================================================
echo.
echo Access points:
echo   Homepage: http://localhost:8000/
echo   Admin Dashboard: http://localhost:8000/dashboard/
echo   User Management: http://localhost:8000/users/management/
echo   Film Management: http://localhost:8000/films/management/
echo   Django Admin: http://localhost:8000/admin/
echo.
echo Test accounts:
echo   Admin: admin / admin123
echo   Staff: john_doe / password123
echo   Staff: bob_manager / password123  
echo   Regular: jane_smith / password123
echo   Regular: alice_user / password123
echo.
echo ==================================================
echo Starting server on http://localhost:8000/
echo Press Ctrl+C to stop the server
echo ==================================================
echo.

python manage.py runserver 8000
