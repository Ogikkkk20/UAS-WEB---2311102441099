#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_django.settings')

try:
    import pymysql
    print("✅ PyMySQL imported successfully!")
    
    # Test PyMySQL connection
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='nazriel2112',
            port=3306
        )
        print("✅ MySQL connection successful!")
        
        # Check if database exists
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES LIKE 'django_blog'")
        result = cursor.fetchone()
        
        if result:
            print("✅ Database 'django_blog' exists!")
        else:
            print("❌ Database 'django_blog' does not exist!")
            print("Creating database...")
            cursor.execute("CREATE DATABASE django_blog")
            print("✅ Database 'django_blog' created!")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        
    # Test Django setup
    try:
        django.setup()
        print("✅ Django setup successful!")
        
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✅ Django database connection successful!")
            
    except Exception as e:
        print(f"❌ Django database connection failed: {e}")
        
except ImportError as e:
    print(f"❌ PyMySQL import failed: {e}")
    print("Please install PyMySQL: pip install pymysql")
