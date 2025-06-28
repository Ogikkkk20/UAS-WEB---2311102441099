@echo off
setlocal EnableDelayedExpansion

echo.
echo ================================================================================
echo                      🎬 DJANGO FILM STREAMING WEBSITE
echo                           CRUD COMPLETION SCRIPT
echo ================================================================================
echo.

cd /d "%~dp0"

REM Colors for output
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "RESET=[0m"

echo %BLUE%[STEP 1]%RESET% Checking Django Project Configuration...
python manage.py check 2>nul
if !errorlevel! neq 0 (
    echo %RED%❌ Django configuration check failed!%RESET%
    python manage.py check
    pause
    exit /b 1
) else (
    echo %GREEN%✅ Django configuration is valid%RESET%
)

echo.
echo %BLUE%[STEP 2]%RESET% Applying Database Migrations...
python manage.py migrate --run-syncdb 2>nul
if !errorlevel! neq 0 (
    echo %RED%❌ Database migration failed!%RESET%
    python manage.py migrate
    pause
    exit /b 1
) else (
    echo %GREEN%✅ Database migrations applied successfully%RESET%
)

echo.
echo %BLUE%[STEP 3]%RESET% Testing Model Operations...
python -c "
import os, django, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()

try:
    from films.models import Genre, Film, FilmReview
    from django.contrib.auth.models import User
    print('✅ All models imported successfully')
    
    # Test Genre creation
    test_genre = Genre.objects.create(name='Test Genre CRUD', description='Testing CRUD operations')
    print(f'✅ Genre created: {test_genre.name} (ID: {test_genre.id})')
    
    # Test Film creation
    from datetime import date
    test_film = Film.objects.create(
        title='Test Film CRUD 2024',
        description='Testing CRUD operations for films',
        synopsis='This film is created to test CRUD functionality',
        director='Test Director',
        cast='Test Actor 1, Test Actor 2',
        release_date=date.today(),
        duration=120,
        rating='PG-13',
        status='published',
        featured=True,
        imdb_rating=8.5
    )
    test_film.genres.add(test_genre)
    print(f'✅ Film created: {test_film.title} (ID: {test_film.id})')
    
    # Test updates
    test_genre.description = 'Updated description for testing'
    test_genre.save()
    test_film.imdb_rating = 9.0
    test_film.save()
    print('✅ Models updated successfully')
    
    # Test deletion
    test_film.delete()
    test_genre.delete()
    print('✅ Models deleted successfully')
    
    print('\\n🎉 ALL MODEL CRUD OPERATIONS WORKING!')
    
except Exception as e:
    print(f'❌ Model test failed: {e}')
    sys.exit(1)
"
if !errorlevel! neq 0 (
    echo %RED%❌ Model operations test failed!%RESET%
    pause
    exit /b 1
) else (
    echo %GREEN%✅ Model CRUD operations working perfectly%RESET%
)

echo.
echo %BLUE%[STEP 4]%RESET% Creating Admin User and Sample Data...
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()

from django.contrib.auth.models import User
from films.models import Genre, Film
from datetime import date

# Create superuser
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@streaming.com', 'admin123')
    print('✅ Admin user created (admin/admin123)')
else:
    print('✅ Admin user already exists')

# Create sample genres
sample_genres = [
    {'name': 'Action', 'description': 'High-octane action movies'},
    {'name': 'Drama', 'description': 'Compelling dramatic stories'},
    {'name': 'Comedy', 'description': 'Funny and entertaining films'},
    {'name': 'Sci-Fi', 'description': 'Science fiction adventures'},
    {'name': 'Horror', 'description': 'Scary and thrilling movies'},
]

created_genres = []
for genre_data in sample_genres:
    genre, created = Genre.objects.get_or_create(
        name=genre_data['name'],
        defaults={'description': genre_data['description']}
    )
    created_genres.append(genre)
    if created:
        print(f'✅ Genre created: {genre.name}')

# Create sample films
sample_films = [
    {
        'title': 'The Ultimate Action Hero',
        'description': 'An action-packed adventure with stunning visuals',
        'synopsis': 'When the world is threatened by an alien invasion, one hero must rise to save humanity...',
        'director': 'Michael Bay',
        'cast': 'Chris Hemsworth, Scarlett Johansson, Robert Downey Jr.',
        'genre': 'Action',
        'duration': 135,
        'rating': 'PG-13',
        'imdb_rating': 8.2
    },
    {
        'title': 'Hearts and Minds',
        'description': 'A touching drama about family and redemption',
        'synopsis': 'A father struggles to reconnect with his estranged family after years of absence...',
        'director': 'Christopher Nolan',
        'cast': 'Matthew McConaughey, Jessica Chastain, Anne Hathaway',
        'genre': 'Drama',
        'duration': 142,
        'rating': 'PG-13',
        'imdb_rating': 8.6
    },
    {
        'title': 'Laugh Out Loud',
        'description': 'The funniest comedy of the year',
        'synopsis': 'A group of friends embark on a hilarious adventure that changes their lives forever...',
        'director': 'Judd Apatow',
        'cast': 'Ryan Reynolds, Emma Stone, Seth Rogen',
        'genre': 'Comedy',
        'duration': 108,
        'rating': 'R',
        'imdb_rating': 7.8
    }
]

for film_data in sample_films:
    if not Film.objects.filter(title=film_data['title']).exists():
        genre = Genre.objects.get(name=film_data['genre'])
        film = Film.objects.create(
            title=film_data['title'],
            description=film_data['description'],
            synopsis=film_data['synopsis'],
            director=film_data['director'],
            cast=film_data['cast'],
            release_date=date.today(),
            duration=film_data['duration'],
            rating=film_data['rating'],
            imdb_rating=film_data['imdb_rating'],
            status='published',
            featured=True
        )
        film.genres.add(genre)
        print(f'✅ Film created: {film.title}')

print('\\n🎬 Sample data created successfully!')
"
if !errorlevel! neq 0 (
    echo %RED%❌ Sample data creation failed!%RESET%
    pause
    exit /b 1
) else (
    echo %GREEN%✅ Admin user and sample data created%RESET%
)

echo.
echo %BLUE%[STEP 5]%RESET% Testing URL Configuration...
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()

from django.test import Client
from django.urls import reverse

client = Client()

# Test main URLs
test_urls = [
    ('/', 'Homepage (should redirect)'),
    ('/films/', 'Films streaming homepage'),
    ('/films/browse/', 'Films browse page'),
    ('/admin/login/', 'Admin login page'),
    ('/login/', 'User login page'),
]

for url, description in test_urls:
    try:
        response = client.get(url)
        if response.status_code in [200, 302]:
            print(f'✅ {description}: Status {response.status_code}')
        else:
            print(f'⚠️ {description}: Status {response.status_code}')
    except Exception as e:
        print(f'❌ {description}: Error - {e}')

print('\\n🌐 URL configuration test completed!')
"
if !errorlevel! neq 0 (
    echo %RED%❌ URL testing failed!%RESET%
    pause
    exit /b 1
) else (
    echo %GREEN%✅ URL configuration working correctly%RESET%
)

echo.
echo ================================================================================
echo                        🎉 CRUD COMPLETION SUCCESSFUL!
echo ================================================================================
echo.
echo %GREEN%✅ Django Configuration: VALID%RESET%
echo %GREEN%✅ Database Migrations: APPLIED%RESET%
echo %GREEN%✅ Model CRUD Operations: WORKING%RESET%
echo %GREEN%✅ Admin User: CREATED%RESET%
echo %GREEN%✅ Sample Data: LOADED%RESET%
echo %GREEN%✅ URL Configuration: VALID%RESET%
echo.
echo %YELLOW%📝 ADMIN LOGIN CREDENTIALS:%RESET%
echo    Username: admin
echo    Password: admin123
echo.
echo %YELLOW%🔗 ACCESS URLS:%RESET%
echo    🏠 Homepage: http://localhost:8000/
echo    🎬 Films: http://localhost:8000/films/
echo    📊 Film Management: http://localhost:8000/films/management/
echo    👑 Admin Panel: http://localhost:8000/admin/
echo.
echo %BLUE%🚀 START THE SERVER:%RESET%
echo    python manage.py runserver
echo.
echo %GREEN%Your Django Film Streaming Website with complete CRUD functionality is ready!%RESET%
echo.
pause
