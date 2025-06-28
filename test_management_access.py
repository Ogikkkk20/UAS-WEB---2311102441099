import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

print("🎬 TESTING FILM MANAGEMENT ACCESS")
print("=" * 40)

# Create test client
client = Client()

print("\n1️⃣ Testing without login...")
response = client.get('/films/management/')
print(f"Status: {response.status_code}")
if response.status_code == 302:
    print(f"Redirect to: {response['Location']}")

print("\n2️⃣ Creating/Getting admin user...")
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
    print("✅ Admin user created")
else:
    print("✅ Admin user exists")

print("\n3️⃣ Testing with admin login...")
login_success = client.login(username='admin', password='admin123')
print(f"Login successful: {login_success}")

if login_success:
    response = client.get('/films/management/')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Film management page accessible!")
        # Check if it contains film management content
        content = response.content.decode('utf-8')
        if 'Film Management' in content:
            print("✅ Content contains 'Film Management'")
        if 'Total Films' in content:
            print("✅ Content contains statistics")
        if 'Add New Film' in content:
            print("✅ Content contains 'Add New Film' button")
    else:
        print(f"❌ Unexpected status: {response.status_code}")

print("\n🏁 Test completed!")
