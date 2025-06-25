from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login

def login(request):
    template_name = "landingpage/login.html"
    pesan = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            pesan = "Username dan password wajib diisi"
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                pesan = "Berhasil login"
                return redirect('/')
            else:
                pesan = "Username atau password salah"
    context = {
        'pesan': pesan
    }
    return render(request, template_name, context)


def registrasi(request):
    template_name = "landingpage/registrasi.html"
    context = {}
    return render(request, template_name, context)
