#!/usr/bin/env python

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()

def test_url_resolution():
    """Test if URLs can be resolved correctly"""
    print("🔍 Testing URL Resolution...")
    
    from django.urls import reverse, NoReverseMatch
    from django.test import Client
    
    # Test URL reverse
    test_urls = [
        ('films:streaming_home', '/films/'),
        ('films:film_management', '/films/management/'),
        ('films:film_list', '/films/browse/'),
    ]
    
    for url_name, expected_path in test_urls:
        try:
            resolved_url = reverse(url_name)
            print(f"✅ {url_name}: {resolved_url}")
            if resolved_url != expected_path:
                print(f"   ⚠️ Expected: {expected_path}")
        except NoReverseMatch as e:
            print(f"❌ {url_name}: {e}")
        except Exception as e:
            print(f"❌ {url_name}: Unexpected error - {e}")
    
    # Test direct URL access
    print("\n🌐 Testing URL Access...")
    client = Client()
    
    test_direct_urls = [
        '/films/',
        '/films/management/',
        '/films/browse/',
    ]
    
    for url in test_direct_urls:
        try:
            response = client.get(url)
            print(f"{'✅' if response.status_code in [200, 302] else '❌'} {url}: Status {response.status_code}")
            if response.status_code == 404:
                print(f"   🔍 404 details: Check if view exists and is properly imported")
        except Exception as e:
            print(f"❌ {url}: Error - {e}")

def test_view_imports():
    """Test if all views can be imported"""
    print("\n📦 Testing View Imports...")
    
    try:
        from films import views
        print("✅ films.views imported successfully")
        
        # Check if required views exist
        required_views = [
            'streaming_home',
            'film_management', 
            'film_list',
            'film_create',
            'film_edit',
            'film_delete'
        ]
        
        for view_name in required_views:
            if hasattr(views, view_name):
                print(f"✅ {view_name}: Available")
            else:
                print(f"❌ {view_name}: Missing")
                
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()

def check_url_patterns():
    """Check URL patterns configuration"""
    print("\n🔗 Checking URL Patterns...")
    
    try:
        from films.urls import urlpatterns
        print(f"✅ Found {len(urlpatterns)} URL patterns in films app")
        
        for pattern in urlpatterns:
            print(f"   - {pattern.pattern} -> {pattern.callback.__name__ if hasattr(pattern, 'callback') else 'Unknown'}")
            
    except Exception as e:
        print(f"❌ URL patterns error: {e}")

if __name__ == "__main__":
    print("🎬 DJANGO URL DEBUGGING SCRIPT")
    print("=" * 50)
    
    test_view_imports()
    check_url_patterns()
    test_url_resolution()
    
    print("\n" + "=" * 50)
    print("🏁 URL Debug Complete")
