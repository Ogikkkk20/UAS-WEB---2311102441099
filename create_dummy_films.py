#!/usr/bin/env python
"""
Script untuk membuat dummy films dan genres
Jalankan dengan: python create_dummy_films.py
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()

from django.contrib.auth.models import User
from films.models import Genre, Film

# Data dummy films
GENRES_DATA = [
    ('Action', 'High-energy films with intense sequences, fights, and adventures'),
    ('Drama', 'Character-driven stories with emotional depth and realistic situations'),
    ('Comedy', 'Humorous films designed to entertain and amuse audiences'),
    ('Horror', 'Films intended to frighten, create suspense, and invoke dread'),
    ('Sci-Fi', 'Science fiction films exploring futuristic concepts and technology'),
    ('Romance', 'Love stories focusing on romantic relationships and emotions'),
    ('Thriller', 'Suspenseful films designed to keep audiences on edge'),
    ('Fantasy', 'Films featuring magical or supernatural elements'),
    ('Documentary', 'Non-fiction films documenting reality and real events'),
    ('Animation', 'Films created using animation techniques'),
    ('Crime', 'Films focused on criminal activities and law enforcement'),
    ('Adventure', 'Films featuring exciting journeys and explorations'),
]

FILMS_DATA = [
    {
        'title': 'Laskar Pelangi 2',
        'director': 'Benni Setiawan',
        'description': 'Sequel dari film terkenal Laskar Pelangi yang mengisahkan petualangan anak-anak Belitung.',
        'synopsis': 'Melanjutkan kisah anak-anak Belitung dalam menggapai mimpi mereka melalui pendidikan dan persahabatan yang kuat.',
        'cast': 'Cut Mini Theo, Lukman Sardi, Tora Sudiro',
        'genres': ['Drama', 'Adventure'],
        'duration': 124,
        'rating': 'PG',
        'imdb_rating': 7.8,
    },
    {
        'title': 'The Raid 3: Final Strike',
        'director': 'Gareth Evans',
        'description': 'Kelanjutan dari franchise action terbaik Indonesia dengan aksi yang lebih intens.',
        'synopsis': 'Rama kembali dalam misi terakhirnya untuk memberantas korupsi di kepolisian dengan pertarungan yang lebih brutal.',
        'cast': 'Iko Uwais, Yayan Ruhian, Cecep Arif Rahman',
        'genres': ['Action', 'Crime', 'Thriller'],
        'duration': 142,
        'rating': 'R',
        'imdb_rating': 8.9,
    },
    {
        'title': 'Habibie & Ainun 3',
        'director': 'Hanung Bramantyo',
        'description': 'Kisah cinta abadi antara BJ Habibie dan Ainun dalam balutan drama romantis.',
        'synopsis': 'Mengisahkan perjalanan cinta Habibie dan Ainun dari masa muda hingga akhir hayat dengan sentuhan yang mengharukan.',
        'cast': 'Reza Rahadian, Bunga Citra Lestari, Tio Pakusadewo',
        'genres': ['Romance', 'Drama'],
        'duration': 117,
        'rating': 'PG',
        'imdb_rating': 8.1,
    },
    {
        'title': 'Pengabdi Setan 3',
        'director': 'Joko Anwar',
        'description': 'Film horror Indonesia yang menggabungkan cerita tradisional dengan teknik sinematografi modern.',
        'synopsis': 'Keluarga yang terkutuk harus menghadapi teror supernatural yang semakin mengerikan dalam rumah tua mereka.',
        'cast': 'Tara Basro, Bront Palarae, Endy Arfian',
        'genres': ['Horror', 'Thriller'],
        'duration': 106,
        'rating': 'R',
        'imdb_rating': 7.5,
    },
    {
        'title': 'Dilan 1993',
        'director': 'Fajar Bustomi',
        'description': 'Kelanjutan kisah cinta Dilan dan Milea di era 90-an yang penuh kenangan.',
        'synopsis': 'Dilan dan Milea menghadapi tantangan baru dalam hubungan mereka saat memasuki kehidupan dewasa.',
        'cast': 'Iqbaal Ramadhan, Vanesha Prescilla, Sissy Prescillia',
        'genres': ['Romance', 'Drama'],
        'duration': 110,
        'rating': 'PG-13',
        'imdb_rating': 7.2,
    },
    {
        'title': 'Si Doel The Movie 3',
        'director': 'Rano Karno',
        'description': 'Petualangan Si Doel dalam menghadapi kehidupan modern di Jakarta.',
        'synopsis': 'Doel harus memilih antara mempertahankan tradisi Betawi atau mengikuti arus modernisasi Jakarta.',
        'cast': 'Rano Karno, Cornelia Agatha, Maudy Koesnaedi',
        'genres': ['Comedy', 'Drama'],
        'duration': 103,
        'rating': 'PG',
        'imdb_rating': 6.8,
    },
    {
        'title': 'Gundala Reborn',
        'director': 'Joko Anwar',
        'description': 'Superhero Indonesia yang bangkit kembali untuk melawan kejahatan di Jakarta.',
        'synopsis': 'Sancaka mendapatkan kekuatan petir dan menjadi Gundala untuk melindungi rakyat dari sindikat kejahatan.',
        'cast': 'Abimana Aryasatya, Tara Basro, Bront Palarae',
        'genres': ['Action', 'Sci-Fi', 'Adventure'],
        'duration': 123,
        'rating': 'PG-13',
        'imdb_rating': 7.4,
    },
    {
        'title': 'Keluarga Cemara 2',
        'director': 'Yandy Laurens',
        'description': 'Kisah keluarga sederhana yang mengajarkan nilai-nilai kehidupan.',
        'synopsis': 'Keluarga Cemara menghadapi cobaan baru sambil tetap mempertahankan kebersamaan dan nilai-nilai keluarga.',
        'cast': 'Ringgo Agus Rahman, Nirina Zubir, Adhisty Zara',
        'genres': ['Drama', 'Comedy'],
        'duration': 108,
        'rating': 'PG',
        'imdb_rating': 7.6,
    },
    {
        'title': 'Yowis Ben 3',
        'director': 'Fajar Nugros',
        'description': 'Komedi Jawa yang mengisahkan perjuangan band indie dalam mencapai kesuksesan.',
        'synopsis': 'Bayu dan teman-temannya berusaha mempertahankan band mereka sambil menghadapi berbagai rintangan hidup.',
        'cast': 'Bayu Skak, Joshua Suherman, Brandon Salim',
        'genres': ['Comedy', 'Drama'],
        'duration': 115,
        'rating': 'PG-13',
        'imdb_rating': 7.0,
    },
    {
        'title': 'Marlina Si Pembunuh dalam Empat Babak',
        'director': 'Mouly Surya',
        'description': 'Film art house Indonesia yang menggabungkan western dengan budaya lokal.',
        'synopsis': 'Marlina melakukan perjalanan untuk mencari keadilan setelah menjadi korban kejahatan di Sumba.',
        'cast': 'Marsha Timothy, Egy Fedly, Yoga Pratama',
        'genres': ['Drama', 'Thriller'],
        'duration': 93,
        'rating': 'R',
        'imdb_rating': 7.8,
    },
]

def create_genres():
    """Membuat genres jika belum ada"""
    print("📂 Creating genres...")
    created_genres = []
    
    for name, description in GENRES_DATA:
        genre, created = Genre.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )
        if created:
            print(f"✅ Created genre: {name}")
            created_genres.append(genre)
        else:
            print(f"📁 Genre exists: {name}")
    
    return Genre.objects.all()

def create_films(count=None):
    """Membuat dummy films"""
    if count is None:
        count = len(FILMS_DATA)
    
    print(f"🎬 Creating {count} films...")
    
    # Ensure we have genres
    genres = create_genres()
    genre_dict = {g.name: g for g in genres}
    
    # Get or create admin user
    try:
        admin_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("✅ Created admin user")
    
    created_films = []
    
    for i, film_data in enumerate(FILMS_DATA[:count]):
        # Generate release date (random in last 5 years)
        release_date = datetime.now().date() - timedelta(
            days=random.randint(30, 1825)  # 1 month to 5 years ago
        )
        
        # Create film
        try:
            film = Film.objects.create(
                title=film_data['title'],
                description=film_data['description'],
                synopsis=film_data['synopsis'],
                director=film_data['director'],
                cast=film_data['cast'],
                release_date=release_date,
                duration=film_data['duration'],
                rating=film_data['rating'],
                imdb_rating=film_data['imdb_rating'],
                status='published',
                featured=random.choice([True, False]),
                views_count=random.randint(100, 5000),
                created_by=admin_user
            )
            
            # Add genres
            film_genres = [genre_dict[g] for g in film_data['genres'] if g in genre_dict]
            film.genres.set(film_genres)
            
            created_films.append(film)
            print(f"✅ Film {i+1}: {film.title} ({film.get_status_display()})")
            
        except Exception as e:
            print(f"❌ Error creating film {i+1}: {e}")
    
    return created_films

def display_summary():
    """Tampilkan ringkasan"""
    total_films = Film.objects.count()
    published_films = Film.objects.filter(status='published').count()
    featured_films = Film.objects.filter(featured=True).count()
    total_genres = Genre.objects.count()
    
    print("\n" + "="*60)
    print("📊 FILM DATABASE SUMMARY")
    print("="*60)
    print(f"🎬 Total Films: {total_films}")
    print(f"📺 Published Films: {published_films}")
    print(f"⭐ Featured Films: {featured_films}")
    print(f"📂 Total Genres: {total_genres}")
    print("="*60)
    
    print("\n📋 RECENT FILMS:")
    print("-"*80)
    for film in Film.objects.all()[:10]:
        status = f"({film.get_status_display()}"
        if film.featured:
            status += ", Featured"
        status += ")"
        
        print(f"🎬 {film.title}")
        print(f"   Director: {film.director} | Rating: {film.rating} | Views: {film.views_count}")
        print(f"   Genres: {film.get_genre_names()} {status}")
        print()

def main():
    print("🎬 FILM DATABASE SETUP")
    print("="*50)
    
    # Check existing data
    existing_films = Film.objects.count()
    existing_genres = Genre.objects.count()
    
    if existing_films > 0:
        print(f"\n⚠️  Found {existing_films} existing films and {existing_genres} genres.")
        print("Options:")
        print("1. Add more films")
        print("2. View summary only")
        print("3. Delete all films and create new")
        
        choice = input("Choose option (1/2/3): ").strip()
        
        if choice == "2":
            display_summary()
            return
        elif choice == "3":
            Film.objects.all().delete()
            print("🗑️  Deleted all existing films")
        elif choice != "1":
            print("Invalid option. Exiting...")
            return
    
    # Create genres first
    create_genres()
    
    # Ask how many films to create
    try:
        count = input(f"\nHow many films to create? (max {len(FILMS_DATA)}, default: all): ").strip()
        if count:
            count = int(count)
            if count > len(FILMS_DATA):
                count = len(FILMS_DATA)
        else:
            count = len(FILMS_DATA)
    except ValueError:
        count = len(FILMS_DATA)
    
    # Create films
    created_films = create_films(count)
    print(f"\n🎉 Successfully created {len(created_films)} films!")
    
    # Display summary
    display_summary()
    
    print("\n🔗 Access URLs:")
    print("   • Film List: http://127.0.0.1:8000/")
    print("   • Film Management: http://127.0.0.1:8000/films/management/")
    print("   • Admin Panel: http://127.0.0.1:8000/admin/")
    print("   • User Management: http://127.0.0.1:8000/users/")
    print("\n🔑 Login Info:")
    print("   • Admin: admin / admin123")

if __name__ == "__main__":
    main()
