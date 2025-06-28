from django.shortcuts import render
from artikel.models import Category, Post, Comment
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='/login/')
def dashboard (request):
    template_name = "dashboard/modern_dashboard.html"
    
    # Import models to get statistics
    try:
        from films.models import Film, FilmReview
        from django.contrib.auth.models import User
        
        total_films = Film.objects.count()
        total_users = User.objects.count()
        total_reviews = FilmReview.objects.count()
        total_views = 0  # You can implement view tracking later
    except ImportError:
        total_films = 0
        total_users = 0
        total_reviews = 0
        total_views = 0
    
    context = {
        "title": "Dashboard",
        "total_films": total_films,
        "total_users": total_users,
        "total_reviews": total_reviews,
        "total_views": total_views,
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
