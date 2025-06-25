from django.shortcuts import render
from artikel.models import Category, Post, Comment

def welcome (request):
    template_name = "landingpage/index.html"
    kategori = Category.objects.all()
    post = Post.objects.all()
    komentar = Comment.objects.all()
    context = {
        "title" : "Top Games",
        "kategori" : kategori,
        "post" : post,
        "komentar" : komentar,
    }
    return render(request, template_name, context)

def dashboard (request):
    template_name = "dashboard/base.html"
    context = {
        "title" : "dashboard"
    }
    return render(request, template_name, context)

def article_detail(request, id):
    template_name = "article_detail.html"
    post = Post.objects.get(id=id)
    komentar = post.comments.all().order_by('-created_at')
    context = {
        "post" : post,
        "komentar" : komentar,
    }
    return render(request, template_name, context)

def cv (request):
    template_name = "cv.html"
    context = {
        "title" : "Dev's CV"
    }
    return render(request, template_name, context)

def rate (request):
    template_name = "rate.html"
    context = {
        "title" : "rate"
    }
    return render(request, template_name, context)

def daftar_artikel(request):
    artikel = artikel.objects.all()
    return render(request, 'dashboard/artikel_list.html', {'artikel': artikel})
