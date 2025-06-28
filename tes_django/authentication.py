from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

def login(request):
    template_name = "admin_login.html"
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, "Username dan password wajib diisi")
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Redirect berdasarkan status user
                if user.is_staff or user.is_superuser:
                    return redirect('/dashboard/')  # Admin ke dashboard
                else:
                    return redirect('films:streaming_home')  # User biasa ke streaming home
            else:
                messages.error(request, "Username atau password salah")
    
    return render(request, template_name)


def registrasi(request):
    template_name = "landingpage/registrasi.html"
    pesan = ""
    
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        # Validasi input
        if not username or not email or not password or not password2:
            pesan = "Semua field wajib diisi"
        elif password != password2:
            pesan = "Password dan konfirmasi password tidak sama"
        elif len(password) < 6:
            pesan = "Password minimal 6 karakter"
        elif User.objects.filter(username=username).exists():
            pesan = "Username sudah digunakan"
        elif User.objects.filter(email=email).exists():
            pesan = "Email sudah digunakan"
        else:
            # Buat user baru
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                # Auto login setelah registrasi
                auth_login(request, user)
                return redirect('dashboard')  # Redirect ke dashboard
            except Exception as e:
                pesan = f"Terjadi kesalahan: {str(e)}"
    
    context = {
        'pesan': pesan
    }
    return render(request, template_name, context)

def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('films:streaming_home')  # Redirect ke homepage streaming
