import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()

from django.test import Client
from django.urls import reverse

print("🔍 TESTING URL ACCESS")
print("=" * 40)

client = Client()

# Test URLs
test_urls = [
    ('/', 'Homepage'),
    ('/films/', 'Films Home'),
    ('/films/management/', 'Film Management (Direct)'),
    ('/management/', 'Management Shortcut'),
    ('/dashboard/', 'Dashboard'),
    ('/admin/login/', 'Admin Login'),
]

print("\n📍 TESTING DIRECT URL ACCESS:")
for url, name in test_urls:
    try:
        response = client.get(url)
        if response.status_code == 200:
            print(f"✅ {name}: {url} - Status 200 (OK)")
        elif response.status_code == 302:
            redirect_url = response.get('Location', 'Unknown')
            print(f"🔄 {name}: {url} - Status 302 (Redirect to: {redirect_url})")
        else:
            print(f"❌ {name}: {url} - Status {response.status_code}")
    except Exception as e:
        print(f"💥 {name}: {url} - Error: {e}")

print("\n📍 TESTING NAMED URL REVERSE:")
try:
    film_mgmt_url = reverse('films:film_management')
    print(f"✅ films:film_management reverses to: {film_mgmt_url}")
    
    response = client.get(film_mgmt_url)
    print(f"✅ films:film_management access: Status {response.status_code}")
    
except Exception as e:
    print(f"❌ films:film_management error: {e}")

print("\n" + "=" * 40)
print("🏁 URL TEST COMPLETED")
