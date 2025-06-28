import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()

from django.urls import resolve
from django.test import Client

print("🔧 TESTING URL RESOLUTION")
print("=" * 30)

# Test URL resolution
test_urls = [
    '/films/',
    '/films/management/',
    '/films/browse/',
    '/films/management/create/',
]

print("1. Testing URL Resolution:")
for url in test_urls:
    try:
        match = resolve(url)
        print(f"✅ {url} -> {match.view_name} ({match.func.__name__})")
    except Exception as e:
        print(f"❌ {url} -> ERROR: {e}")

print("\n2. Testing HTTP Responses:")
client = Client()
for url in test_urls:
    try:
        response = client.get(url)
        if response.status_code == 200:
            print(f"✅ {url} -> Status 200 (OK)")
        elif response.status_code == 302:
            print(f"🔄 {url} -> Status 302 (Redirect)")
        else:
            print(f"⚠️ {url} -> Status {response.status_code}")
    except Exception as e:
        print(f"❌ {url} -> ERROR: {e}")

print("\n🏁 Test completed!")
