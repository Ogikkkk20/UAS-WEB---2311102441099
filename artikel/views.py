# views.py
from django.shortcuts import render
from .models import Category

def admin_kategori_list(request):
    kategoris = Category.objects.all()
    return render(request, 'admin/kategori_list.html', {'kategoris': kategoris})
