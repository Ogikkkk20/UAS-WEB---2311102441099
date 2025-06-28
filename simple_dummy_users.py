#!/usr/bin/env python
"""
Script sederhana untuk membuat dummy users tanpa dependencies eksternal
Jalankan dengan: python simple_dummy_users.py
"""

import os
import sys
import django
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')
django.setup()

from django.contrib.auth.models import User

# Data dummy Indonesia
FIRST_NAMES = [
    'Andi', 'Budi', 'Citra', 'Dewi', 'Eko', 'Fitri', 'Gita', 'Hani', 'Indra', 'Joko',
    'Kartika', 'Lili', 'Maya', 'Nina', 'Omar', 'Putri', 'Qori', 'Rina', 'Sari', 'Toni',
    'Umar', 'Vera', 'Wati', 'Yani', 'Zaki', 'Ahmad', 'Bayu', 'Candra', 'Dian', 'Erika',
    'Farhan', 'Gina', 'Hasan', 'Ira', 'Jihan', 'Kiki', 'Luna', 'Mila', 'Nanda', 'Ovi'
]

LAST_NAMES = [
    'Pratama', 'Sari', 'Wijaya', 'Putri', 'Santoso', 'Wati', 'Kusuma', 'Dewi', 'Saputra', 'Maharani',
    'Hidayat', 'Permata', 'Nugroho', 'Cahaya', 'Purnama', 'Indah', 'Hakim', 'Anggraini', 'Rahman', 'Safitri',
    'Setiawan', 'Melati', 'Firmansyah', 'Lestari', 'Gunawan', 'Rahayu', 'Kurniawan', 'Handayani', 'Susanto', 'Puspita'
]

DOMAINS = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'mail.com']

def create_dummy_users(count=15):
    """Membuat dummy users"""
    print(f"🚀 Membuat {count} dummy users...")
    
    created_users = []
    
    for i in range(count):
        # Generate data random
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        username = f"{first_name.lower()}{last_name.lower()}{random.randint(1, 999)}"
        domain = random.choice(DOMAINS)
        email = f"{username}@{domain}"
        
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
            email = f"{username}{counter}@{domain}"
            counter += 1
        
        try:
            # Buat user dengan random properties
            is_staff = random.choice([True, False]) if i > 5 else False  # Beberapa user jadi staff
            is_active = random.choice([True, True, True, False])  # Mayoritas aktif
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password='password123',  # Password default untuk semua dummy users
                first_name=first_name,
                last_name=last_name,
                is_active=is_active,
                is_staff=is_staff,
            )
            
            created_users.append(user)
            status = "✅"
            if not is_active:
                status += " (Inactive)"
            if is_staff:
                status += " (Staff)"
                
            print(f"{status} User {i+1}: {username} ({first_name} {last_name}) - {email}")
            
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
    active_users = User.objects.filter(is_active=True).count()
    inactive_users = User.objects.filter(is_active=False).count()
    
    print("\n" + "="*60)
    print("📊 RINGKASAN DATABASE USERS")
    print("="*60)
    print(f"👥 Total Users: {total_users}")
    print(f"👑 Admin Users: {admin_users}")
    print(f"⚙️  Staff Users: {staff_users}")
    print(f"👤 Regular Users: {regular_users}")
    print(f"🟢 Active Users: {active_users}")
    print(f"🔴 Inactive Users: {inactive_users}")
    print("="*60)
    
    print("\n📋 DAFTAR USERS:")
    print("-"*90)
    print(f"{'ID':<4} {'Username':<20} {'Name':<25} {'Email':<25} {'Status':<15}")
    print("-"*90)
    
    for user in User.objects.all().order_by('id'):
        status_parts = []
        if user.is_superuser:
            status_parts.append("Admin")
        elif user.is_staff:
            status_parts.append("Staff")
        else:
            status_parts.append("User")
            
        if not user.is_active:
            status_parts.append("Inactive")
        
        status = ", ".join(status_parts)
        full_name = f"{user.first_name} {user.last_name}".strip()
        if not full_name:
            full_name = "-"
        
        print(f"{user.id:<4} {user.username:<20} {full_name:<25} {user.email:<25} {status:<15}")

def main():
    print("🗄️  DJANGO USER DATABASE SETUP")
    print("="*60)
    
    # Buat admin user
    create_admin_user()
    
    # Cek apakah sudah ada users (selain admin)
    existing_users = User.objects.filter(is_superuser=False).count()
    
    if existing_users > 0:
        print(f"\n⚠️  Sudah ada {existing_users} non-admin users di database.")
        print("Pilihan:")
        print("1. Tambah lebih banyak users")
        print("2. Lihat ringkasan saja")
        print("3. Hapus semua non-admin users dan buat baru")
        
        choice = input("Pilih opsi (1/2/3): ").strip()
        
        if choice == "2":
            display_users_summary()
            return
        elif choice == "3":
            # Hapus semua non-admin users
            deleted_count = User.objects.filter(is_superuser=False).count()
            User.objects.filter(is_superuser=False).delete()
            print(f"🗑️  Dihapus {deleted_count} non-admin users")
        elif choice != "1":
            print("Opsi tidak valid. Keluar...")
            return
    
    # Tanya berapa users yang mau dibuat
    try:
        count = input("\nBerapa dummy users yang ingin dibuat? (default: 15): ")
        count = int(count) if count.strip() else 15
        
        if count <= 0:
            print("Jumlah harus lebih dari 0")
            return
            
    except ValueError:
        count = 15
    
    # Buat dummy users
    print(f"\n🚀 Membuat {count} dummy users...")
    created_users = create_dummy_users(count)
    print(f"\n🎉 Berhasil membuat {len(created_users)} dummy users!")
    
    # Tampilkan ringkasan
    display_users_summary()
    
    print("\n🔗 Akses URLs:")
    print("   • Home: http://127.0.0.1:8000")
    print("   • User Management: http://127.0.0.1:8000/users/")
    print("   • Admin Panel: http://127.0.0.1:8000/admin/")
    print("   • Database View: http://127.0.0.1:8000/database/")
    print("\n🔑 Login Info:")
    print("   • Admin: admin / admin123")
    print("   • Dummy Users: [username] / password123")

if __name__ == "__main__":
    main()
