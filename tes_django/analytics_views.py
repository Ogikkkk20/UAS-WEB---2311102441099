from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count, Q
from datetime import datetime, timedelta

def is_admin_or_staff(user):
    """Check if user is admin or staff"""
    return user.is_authenticated and (user.is_superuser or user.is_staff)

@login_required
@user_passes_test(is_admin_or_staff)
def analytics(request):
    """Analytics dashboard"""
    try:
        from films.models import Film, FilmReview
        
        # Basic stats
        total_films = Film.objects.count()
        total_users = User.objects.count()
        total_reviews = FilmReview.objects.count()
        
        # Get recent data (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        # Growth stats
        recent_films = Film.objects.filter(created_at__gte=thirty_days_ago).count()
        recent_users = User.objects.filter(date_joined__gte=thirty_days_ago).count()
        recent_reviews = FilmReview.objects.filter(created_at__gte=thirty_days_ago).count()
        
        # Popular genres
        popular_genres = Film.objects.values('genres__name').annotate(
            count=Count('genres__name')
        ).order_by('-count')[:5]
        
        # Recent activity (last 10 items)
        recent_activities = []
        
        # Recent films
        recent_films_list = Film.objects.select_related('created_by').order_by('-created_at')[:5]
        for film in recent_films_list:
            recent_activities.append({
                'type': 'film',
                'title': f'New film "{film.title}" uploaded',
                'time': film.created_at,
                'icon': 'fas fa-film',
                'color': 'blue'
            })
        
        # Recent users
        recent_users_list = User.objects.order_by('-date_joined')[:5]
        for user in recent_users_list:
            recent_activities.append({
                'type': 'user',
                'title': f'New user "{user.username}" registered',
                'time': user.date_joined,
                'icon': 'fas fa-user',
                'color': 'green'
            })
        
        # Sort by time
        recent_activities.sort(key=lambda x: x['time'], reverse=True)
        recent_activities = recent_activities[:10]
        
    except ImportError:
        total_films = 0
        total_users = 0
        total_reviews = 0
        recent_films = 0
        recent_users = 0
        recent_reviews = 0
        popular_genres = []
        recent_activities = []
    
    context = {
        'total_films': total_films,
        'total_users': total_users,
        'total_reviews': total_reviews,
        'recent_films': recent_films,
        'recent_users': recent_users,
        'recent_reviews': recent_reviews,
        'popular_genres': popular_genres,
        'recent_activities': recent_activities,
    }
    
    return render(request, 'dashboard/modern_analytics.html', context)
