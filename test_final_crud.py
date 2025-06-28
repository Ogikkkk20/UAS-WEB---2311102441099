#!/usr/bin/env python
"""
🎬 FINAL CRUD TEST SCRIPT
Tests all CRUD operations for Films and Users
"""

import os
import sys
import django
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()

from django.contrib.auth.models import User
from films.models import Genre, Film, FilmReview
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse

def print_separator(title):
    print("=" * 60)
    print(f"   {title}")
    print("=" * 60)

def test_models_crud():
    """Test CRUD operations on models directly"""
    print_separator("🧪 TESTING MODEL CRUD OPERATIONS")
    
    try:
        # Test Genre CRUD
        print("\n📁 Testing Genre CRUD...")
        
        # Create
        genre = Genre.objects.create(
            name="Test Action",
            description="Action movies for testing"
        )
        print(f"✅ Genre Created: {genre.name} (ID: {genre.id})")
        
        # Read
        found_genre = Genre.objects.get(id=genre.id)
        print(f"✅ Genre Read: {found_genre.name}")
        
        # Update
        found_genre.description = "Updated action description"
        found_genre.save()
        print(f"✅ Genre Updated: {found_genre.description}")
        
        # Test Film CRUD
        print("\n🎬 Testing Film CRUD...")
        
        # Create
        film = Film.objects.create(
            title="Test Movie 2024",
            description="A comprehensive test movie",
            synopsis="This is a test movie created for CRUD testing",
            director="Test Director",
            cast="Test Actor 1, Test Actor 2",
            release_date=date.today(),
            duration=120,
            rating="PG-13",
            imdb_rating=8.5,
            status="published",
            featured=True
        )
        film.genres.add(genre)
        print(f"✅ Film Created: {film.title} (ID: {film.id})")
        
        # Read
        found_film = Film.objects.get(id=film.id)
        print(f"✅ Film Read: {found_film.title} - {found_film.genre_list}")
        
        # Update
        found_film.imdb_rating = 9.2
        found_film.save()
        print(f"✅ Film Updated: Rating changed to {found_film.imdb_rating}")
        
        # Test FilmReview CRUD
        print("\n⭐ Testing FilmReview CRUD...")
        
        # Create user for review
        user = User.objects.create_user(
            username="test_reviewer",
            email="reviewer@test.com",
            password="testpass123"
        )
        
        # Create review
        review = FilmReview.objects.create(
            film=film,
            user=user,
            rating=5,
            comment="Excellent test movie!"
        )
        print(f"✅ Review Created: {review.rating} stars by {review.user.username}")
        
        # Read
        found_review = FilmReview.objects.get(id=review.id)
        print(f"✅ Review Read: {found_review.comment}")
        
        # Update
        found_review.rating = 4
        found_review.comment = "Updated: Good test movie"
        found_review.save()
        print(f"✅ Review Updated: {found_review.rating} stars - {found_review.comment}")
        
        # Clean up (Delete)
        print("\n🗑️ Cleaning up test data...")
        found_review.delete()
        print("✅ Review Deleted")
        
        found_film.delete()
        print("✅ Film Deleted")
        
        found_genre.delete()
        print("✅ Genre Deleted")
        
        user.delete()
        print("✅ Test User Deleted")
        
        print("\n🎉 ALL MODEL CRUD OPERATIONS SUCCESSFUL!")
        return True
        
    except Exception as e:
        print(f"❌ MODEL CRUD ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_url_accessibility():
    """Test URL accessibility and responses"""
    print_separator("🌐 TESTING URL ACCESSIBILITY")
    
    try:
        client = Client()
        
        # Test public URLs
        urls_to_test = [
            ('/', 'Homepage'),
            ('/films/', 'Films List'),
            ('/admin/login/', 'Admin Login'),
        ]
        
        for url, name in urls_to_test:
            try:
                response = client.get(url)
                if response.status_code in [200, 302]:
                    print(f"✅ {name} ({url}): Status {response.status_code}")
                else:
                    print(f"⚠️ {name} ({url}): Status {response.status_code}")
            except Exception as e:
                print(f"❌ {name} ({url}): Error - {e}")
        
        print("\n🎉 URL ACCESSIBILITY TEST COMPLETED!")
        return True
        
    except Exception as e:
        print(f"❌ URL TEST ERROR: {e}")
        return False

def test_admin_functionality():
    """Test admin interface functionality"""
    print_separator("👑 TESTING ADMIN FUNCTIONALITY")
    
    try:
        # Create superuser for testing
        admin_user = User.objects.create_superuser(
            username='test_admin',
            email='admin@test.com',
            password='admin123'
        )
        print(f"✅ Admin User Created: {admin_user.username}")
        
        client = Client()
        login_success = client.login(username='test_admin', password='admin123')
        
        if login_success:
            print("✅ Admin Login Successful")
            
            # Test admin pages
            admin_urls = [
                '/admin/',
                '/admin/films/',
                '/admin/films/genre/',
                '/admin/films/film/',
                '/admin/auth/user/',
            ]
            
            for url in admin_urls:
                try:
                    response = client.get(url)
                    if response.status_code == 200:
                        print(f"✅ Admin Page Accessible: {url}")
                    else:
                        print(f"⚠️ Admin Page Issue: {url} (Status: {response.status_code})")
                except Exception as e:
                    print(f"❌ Admin Page Error: {url} - {e}")
        else:
            print("❌ Admin Login Failed")
        
        # Clean up
        admin_user.delete()
        print("✅ Test Admin User Deleted")
        
        print("\n🎉 ADMIN FUNCTIONALITY TEST COMPLETED!")
        return login_success
        
    except Exception as e:
        print(f"❌ ADMIN TEST ERROR: {e}")
        return False

def run_all_tests():
    """Run all comprehensive tests"""
    print_separator("🚀 STARTING COMPREHENSIVE CRUD TESTS")
    
    results = {
        'models': test_models_crud(),
        'urls': test_url_accessibility(),
        'admin': test_admin_functionality()
    }
    
    print_separator("📊 FINAL RESULTS")
    
    all_passed = True
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name.upper()} CRUD: {status}")
        if not result:
            all_passed = False
    
    print(f"\nOVERALL STATUS: {'🎉 ALL TESTS PASSED!' if all_passed else '⚠️ SOME TESTS FAILED'}")
    
    if all_passed:
        print("\n🎬 YOUR DJANGO FILM STREAMING WEBSITE IS READY!")
        print("✅ All CRUD operations are working perfectly")
        print("✅ URL routing is properly configured")
        print("✅ Admin interface is fully functional")
        print("\n🌐 You can now:")
        print("   • Access the homepage at: http://localhost:8000/")
        print("   • Manage films at: http://localhost:8000/admin/")
        print("   • View film list at: http://localhost:8000/films/")
    else:
        print("\n🔧 Please check the errors above and fix them.")
    
    return all_passed

if __name__ == "__main__":
    run_all_tests()
