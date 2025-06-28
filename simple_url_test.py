import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()

from django.test import Client
from django.urls import reverse

print("🎬 TESTING DJANGO FILM MANAGEMENT")
print("=" * 40)

client = Client()

# Test URLs
test_urls = [
    ('/films/', 'Films Home'),
    ('/films/management/', 'Film Management'),
    ('/films/browse/', 'Films Browse'),
]

for url, name in test_urls:
    try:
        response = client.get(url)
        status = response.status_code
        if status == 200:
            print(f"✅ {name}: OK (Status {status})")
        elif status == 302:
            print(f"🔄 {name}: Redirect (Status {status})")
        else:
            print(f"❌ {name}: Error (Status {status})")
    except Exception as e:
        print(f"❌ {name}: Exception - {e}")

print("\n🔍 Testing URL reversing...")
try:
    film_mgmt_url = reverse('films:film_management')
    print(f"✅ films:film_management resolves to: {film_mgmt_url}")
except Exception as e:
    print(f"❌ URL reverse error: {e}")

print("\n🏁 Test completed!")
