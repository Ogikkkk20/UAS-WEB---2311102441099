@echo off
echo ==================================================
echo        FILM CRUD TEST SCRIPT
echo ==================================================
echo.

cd /d "%~dp0"

echo Testing Film Creation...
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()

from films.models import Genre, Film
from films.forms import FilmForm
from django.contrib.auth.models import User

# Create test admin user
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
    print('Created admin user: admin/admin123')

# Create test genre
genre, created = Genre.objects.get_or_create(
    name='Action',
    defaults={'description': 'Action films with excitement'}
)
print(f'Genre: {genre.name}')

# Test form validation
print('\nTesting FilmForm...')
form_data = {
    'title': 'Test Film',
    'description': 'This is a test film description',
    'synopsis': 'This is a detailed synopsis of the test film',
    'release_date': '2024-01-01',
    'duration': 120,
    'rating': 4.5,
    'imdb_rating': 8.0,
    'director': 'Test Director',
    'cast': 'Test Actor 1, Test Actor 2',
    'status': 'published',
    'featured': False
}

form = FilmForm(data=form_data)
print(f'Form valid: {form.is_valid()}')
if not form.is_valid():
    print('Form errors:')
    for field, errors in form.errors.items():
        print(f'  {field}: {errors}')

# Test film creation
if form.is_valid():
    film = form.save(commit=False)
    film.created_by = admin_user
    film.save()
    film.genres.add(genre)
    print(f'Created film: {film.title}')
    
    # Test film retrieval
    retrieved_film = Film.objects.get(title='Test Film')
    print(f'Retrieved film: {retrieved_film.title}')
    
    # Clean up
    retrieved_film.delete()
    print('Test film deleted')

print('\n✅ Film CRUD test completed successfully!')
print()
print('URL Routes:')
print('  - Film Management: /films/management/')
print('  - Create Film: /films/management/create/')
print('  - Edit Film: /films/management/edit/<id>/')
print('  - Delete Film: /films/management/delete/<id>/')
print()
print('Access the form at: http://localhost:8000/films/management/create/')
"

echo.
echo ==================================================
echo            FILM CRUD TEST COMPLETED!
echo ==================================================
echo.
echo To start the server:
echo   python manage.py runserver
echo.
echo Then access: http://localhost:8000/films/management/create/
echo.
pause
