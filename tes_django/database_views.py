from django.shortcuts import render
from django.contrib.auth.models import User
from artikel.models import Category, Post, Comment
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def database_view(request):
    """View untuk melihat data database"""
    
    # Ambil data dari database
    users = User.objects.all()
    categories = Category.objects.all()
    posts = Post.objects.all()
    comments = Comment.objects.all()
    
    context = {
        'users': users,
        'categories': categories,
        'posts': posts,
        'comments': comments,
        'user_count': users.count(),
        'category_count': categories.count(),
        'post_count': posts.count(),
        'comment_count': comments.count(),
    }
    
    return render(request, 'database_view.html', context)
