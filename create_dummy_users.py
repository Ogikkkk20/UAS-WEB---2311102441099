#!/usr/bin/env python
"""
Script untuk membuat dummy users di Django
Jalankan dengan: python manage.py shell < create_dummy_users.py
Atau: python create_dummy_users.py
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()

from django.contrib.auth.models import User
from faker import Faker
import random

# Inisialisasi Faker untuk data dummy
fake = Faker('id_ID')  # Gunakan locale Indonesia

def create_dummy_users(count=20):
    """Membuat dummy users"""
    print(f"🚀 Membuat {count} dummy users...")
    
    created_users = []
    
    for i in range(count):
        # Generate data random
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"{first_name.lower()}{last_name.lower()}{random.randint(1, 999)}"
        email = f"{username}@{fake.domain_name()}"
        
        # Pastikan username unik
        counter = 1
        original_username = username
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1
        
        # Pastikan email unik
        counter = 1
        original_email = email
        while User.objects.filter(email=email).exists():
            email = f"{username}{counter}@{fake.domain_name()}"
            counter += 1
        
        try:
            # Buat user
            user = User.objects.create_user(
                username=username,
                email=email,
                password='password123',  # Password default untuk semua dummy users
                first_name=first_name,
                last_name=last_name,
                is_active=True,
                is_staff=random.choice([True, False]) if i > 10 else False,  # Beberapa user jadi staff
            )
            
            created_users.append(user)
            print(f"✅ User {i+1}: {username} ({first_name} {last_name}) - {email}")
            
        except Exception as e:
            print(f"❌ Error creating user {i+1}: {e}")
    
    return created_users

def create_admin_user():
    """Membuat admin user jika belum ada"""
    print("👤 Checking admin user...")
    
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print("✅ Admin user created: admin/admin123")
        return admin
    else:
        print("✅ Admin user already exists")
        return User.objects.get(username='admin')

def display_users_summary():
    """Tampilkan ringkasan users"""
    total_users = User.objects.count()
    admin_users = User.objects.filter(is_superuser=True).count()
    staff_users = User.objects.filter(is_staff=True, is_superuser=False).count()
    regular_users = User.objects.filter(is_staff=False, is_superuser=False).count()
    
    print("\n" + "="*50)
    print("📊 RINGKASAN DATABASE USERS")
    print("="*50)
    print(f"👥 Total Users: {total_users}")
    print(f"👑 Admin Users: {admin_users}")
    print(f"⚙️  Staff Users: {staff_users}")
    print(f"👤 Regular Users: {regular_users}")
    print("="*50)
    
    print("\n📋 DAFTAR USERS:")
    print("-"*80)
    print(f"{'ID':<4} {'Username':<20} {'Name':<25} {'Email':<25} {'Type':<10}")
    print("-"*80)
    
    for user in User.objects.all().order_by('id'):
        user_type = "Admin" if user.is_superuser else ("Staff" if user.is_staff else "User")
        full_name = f"{user.first_name} {user.last_name}".strip()
        if not full_name:
            full_name = "-"
        
        print(f"{user.id:<4} {user.username:<20} {full_name:<25} {user.email:<25} {user_type:<10}")

def main():
    print("🗄️  DJANGO USER DATABASE SETUP")
    print("="*50)
    
    # Buat admin user
    create_admin_user()
    
    # Cek apakah sudah ada users (selain admin)
    existing_users = User.objects.filter(is_superuser=False).count()
    
    if existing_users > 0:
        print(f"\n⚠️  Sudah ada {existing_users} users di database.")
        response = input("Apakah ingin menambah lebih banyak users? (y/n): ")
        if response.lower() != 'y':
            display_users_summary()
            return
    
    # Tanya berapa users yang mau dibuat
    try:
        count = input("\nBerapa dummy users yang ingin dibuat? (default: 20): ")
        count = int(count) if count.strip() else 20
    except ValueError:
        count = 20
    
    # Buat dummy users
    if count > 0:
        try:
            # Install faker jika belum ada
            try:
                import faker
            except ImportError:
                print("📦 Installing Faker library...")
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", "faker"])
                import faker
                print("✅ Faker installed successfully!")
            
            created_users = create_dummy_users(count)
            print(f"\n🎉 Berhasil membuat {len(created_users)} dummy users!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Coba install faker manually: pip install faker")
    
    # Tampilkan ringkasan
    display_users_summary()
    
    print("\n🔗 Akses URLs:")
    print("   • Admin Panel: http://127.0.0.1:8000/admin/")
    print("   • Database View: http://127.0.0.1:8000/database/")
    print("   • User Management: http://127.0.0.1:8000/users/")
    print("\n🔑 Login Info:")
    print("   • Admin: admin / admin123")
    print("   • Dummy Users: [username] / password123")

if __name__ == "__main__":
    main()
