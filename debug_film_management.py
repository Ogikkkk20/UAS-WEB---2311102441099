import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()

from films.views import film_management, is_staff_user
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.contrib.auth import authenticate, login

print("🔍 DEBUGGING FILM MANAGEMENT VIEW")
print("=" * 50)

print("\n1️⃣ Testing function imports...")
print(f"✅ film_management function: {film_management}")
print(f"✅ is_staff_user function: {is_staff_user}")

print("\n2️⃣ Creating test user...")
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

print(f"Admin user: {admin_user.username}")
print(f"Is staff: {admin_user.is_staff}")
print(f"Is superuser: {admin_user.is_superuser}")

print("\n3️⃣ Testing staff check function...")
print(f"is_staff_user result: {is_staff_user(admin_user)}")

print("\n4️⃣ Testing URL resolution...")
from django.urls import reverse
try:
    url = reverse('films:film_management')
    print(f"✅ films:film_management resolves to: {url}")
except Exception as e:
    print(f"❌ URL resolution error: {e}")

print("\n5️⃣ Checking template existence...")
import os
template_path = 'c:/Users/nazri/OneDrive/Desktop/joki uas/2311102441099-Ogi-Febrian-Saputra/templates/dashboard/film_management.html'
if os.path.exists(template_path):
    print("✅ Template exists")
    # Read first few lines to verify content
    with open(template_path, 'r', encoding='utf-8') as f:
        first_lines = ''.join(f.readlines()[:5])
        print(f"Template starts with: {first_lines[:100]}...")
else:
    print("❌ Template not found")

print("\n6️⃣ Testing view directly...")
# Create mock request
request = HttpRequest()
request.method = 'GET'
request.user = admin_user

try:
    response = film_management(request)
    print(f"✅ View executed successfully")
    print(f"Response type: {type(response)}")
    if hasattr(response, 'status_code'):
        print(f"Status code: {response.status_code}")
    if hasattr(response, 'context_data'):
        print(f"Context keys: {list(response.context_data.keys())}")
except Exception as e:
    print(f"❌ View execution error: {e}")
    import traceback
    traceback.print_exc()

print("\n🏁 Debug completed!")
