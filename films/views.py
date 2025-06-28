from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import os
import tempfile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .models import Film, Genre, FilmReview
from .forms import FilmForm, GenreForm, FilmReviewForm, FilmSearchForm

def is_staff_user(user):
    """Check if user is staff or admin"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# Public Views
def film_list(request):
    """Public film listing page"""
    films = Film.objects.filter(status='published').select_related('created_by').prefetch_related('genres')
    genres = Genre.objects.all()
    
    # Search and filtering
    search_form = FilmSearchForm(request.GET)
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        genre = search_form.cleaned_data.get('genre')
        rating = search_form.cleaned_data.get('rating')
        sort_by = search_form.cleaned_data.get('sort_by') or '-created_at'
        
        if search:
            films = films.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(director__icontains=search) |
                Q(cast__icontains=search)
            )
        
        if genre:
            films = films.filter(genres=genre)
        
        if rating:
            films = films.filter(rating=rating)
        
        films = films.order_by(sort_by)
    
    # Featured films
    featured_films = films.filter(featured=True)[:6]
    
    # Pagination
    paginator = Paginator(films, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'featured_films': featured_films,
        'genres': genres,
        'search_form': search_form,
        'total_films': films.count(),
    }
    
    return render(request, 'films/film_list.html', context)

def film_detail(request, slug):
    """Enhanced film detail page for streaming"""
    film = get_object_or_404(Film, slug=slug, status='published')
    
    # Get recommended films (same genres, excluding current film)
    recommended_films = Film.objects.filter(
        status='published',
        genres__in=film.genres.all()
    ).exclude(id=film.id).distinct()[:8]
    
    # Get reviews
    reviews = film.reviews.filter(approved=True).select_related('user').order_by('-created_at')[:10]
    
    # Calculate average rating
    avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
    
    context = {
        'film': film,
        'recommended_films': recommended_films,
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    return render(request, 'watch_movie.html', context)

@login_required
@require_POST
def add_review(request, slug):
    """Add film review"""
    film = get_object_or_404(Film, slug=slug, status='published')
    
    # Check if user already reviewed
    if FilmReview.objects.filter(film=film, user=request.user).exists():
        messages.error(request, 'You have already reviewed this film.')
        return redirect('film_detail', slug=slug)
    
    form = FilmReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.film = film
        review.user = request.user
        review.save()
        messages.success(request, 'Your review has been submitted and is pending approval.')
    else:
        messages.error(request, 'Please correct the errors in your review.')
    
    return redirect('film_detail', slug=slug)

# Management Views (Staff Only)
@login_required
@user_passes_test(is_staff_user)
def film_management(request):
    """Film management dashboard"""
    films = Film.objects.select_related('created_by').prefetch_related('genres')
    
    # Search and filtering
    search_form = FilmSearchForm(request.GET)
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        genre = search_form.cleaned_data.get('genre')
        rating = search_form.cleaned_data.get('rating')
        status = search_form.cleaned_data.get('status')
        sort_by = search_form.cleaned_data.get('sort_by') or '-created_at'
        
        if search:
            films = films.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(director__icontains=search)
            )
        
        if genre:
            films = films.filter(genres=genre)
        
        if rating:
            films = films.filter(rating=rating)
            
        if status:
            films = films.filter(status=status)
        
        films = films.order_by(sort_by)
    
    # Statistics
    stats = {
        'total': Film.objects.count(),
        'published': Film.objects.filter(status='published').count(),
        'draft': Film.objects.filter(status='draft').count(),
        'featured': Film.objects.filter(featured=True).count(),
        'with_video': Film.objects.exclude(video_file='').count(),
    }
    
    # Pagination
    paginator = Paginator(films, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'stats': stats,
        'title': 'Film Management',
        'breadcrumb': 'Film Management'
    }
    
    return render(request, 'dashboard/modern_film_management.html', context)

@login_required
@user_passes_test(is_staff_user)
def film_create(request):
    """Create new film"""
    if request.method == 'POST':
        print("=== DEBUG FILM CREATE ===")
        print("POST Data:", request.POST)
        print("FILES Data:", request.FILES)
        
        form = FilmForm(request.POST, request.FILES)
        print("Form is valid:", form.is_valid())
        if not form.is_valid():
            print("Form errors:", form.errors)
            
        if form.is_valid():
            film = form.save(commit=False)
            film.created_by = request.user
            
            # Handle AJAX uploaded files
            video_path = form.cleaned_data.get('video_path')
            poster_path = form.cleaned_data.get('poster_path')
            
            print("Video path:", video_path)
            print("Poster path:", poster_path)
            
            if video_path and not film.video_file:
                # Move video from temp to permanent location
                temp_path = video_path
                permanent_path = f'films/{temp_path.split("/")[-1]}'
                print(f"Moving video from {temp_path} to {permanent_path}")
                if default_storage.exists(temp_path):
                    content = default_storage.open(temp_path).read()
                    film.video_file.save(permanent_path.split('/')[-1], ContentFile(content))
                    default_storage.delete(temp_path)  # Clean up temp file
            
            if poster_path and not film.poster:
                # Move poster from temp to permanent location
                temp_path = poster_path
                permanent_path = f'film_posters/{temp_path.split("/")[-1]}'
                print(f"Moving poster from {temp_path} to {permanent_path}")
                if default_storage.exists(temp_path):
                    content = default_storage.open(temp_path).read()
                    film.poster.save(permanent_path.split('/')[-1], ContentFile(content))
                    default_storage.delete(temp_path)  # Clean up temp file
            
            film.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, f'Film "{film.title}" has been created successfully.')
            return redirect('films:film_management')
        else:
            print("Form validation failed")
    else:
        form = FilmForm()
    
    context = {
        'form': form,
        'title': 'Add New Film',
        'action': 'Create',
        'button_text': 'Create Film',
    }
    
    return render(request, 'dashboard/modern_film_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def film_edit(request, id):
    """Edit existing film"""
    film = get_object_or_404(Film, id=id)
    
    if request.method == 'POST':
        print("=== DEBUG FILM EDIT ===")
        print("POST Data:", request.POST)
        print("FILES Data:", request.FILES)
        
        form = FilmForm(request.POST, request.FILES, instance=film)
        print("Form is valid:", form.is_valid())
        if not form.is_valid():
            print("Form errors:", form.errors)
            
        if form.is_valid():
            # Handle AJAX uploaded files
            video_path = form.cleaned_data.get('video_path')
            poster_path = form.cleaned_data.get('poster_path')
            
            print("Video path:", video_path)
            print("Poster path:", poster_path)
            
            if video_path:
                # Move video from temp to permanent location
                temp_path = video_path
                permanent_path = f'films/{temp_path.split("/")[-1]}'
                print(f"Moving video from {temp_path} to {permanent_path}")
                if default_storage.exists(temp_path):
                    content = default_storage.open(temp_path).read()
                    film.video_file.save(permanent_path.split('/')[-1], ContentFile(content))
                    default_storage.delete(temp_path)  # Clean up temp file
            
            if poster_path:
                # Move poster from temp to permanent location
                temp_path = poster_path
                permanent_path = f'film_posters/{temp_path.split("/")[-1]}'
                print(f"Moving poster from {temp_path} to {permanent_path}")
                if default_storage.exists(temp_path):
                    content = default_storage.open(temp_path).read()
                    film.poster.save(permanent_path.split('/')[-1], ContentFile(content))
                    default_storage.delete(temp_path)  # Clean up temp file
            
            form.save()
            messages.success(request, f'Film "{film.title}" has been updated successfully.')
            return redirect('films:film_management')
        else:
            print("Form validation failed in edit")
    else:
        form = FilmForm(instance=film)
    
    context = {
        'form': form,
        'film': film,
        'title': f'Edit {film.title}',
        'action': 'Update',
        'button_text': 'Update Film',
    }
    
    return render(request, 'dashboard/modern_film_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def film_delete(request, id):
    """Delete film"""
    film = get_object_or_404(Film, id=id)
    
    if request.method == 'POST':
        title = film.title
        film.delete()
        messages.success(request, f'Film "{title}" has been deleted successfully.')
        return redirect('film_management')
    
    context = {
        'film': film,
    }
    
    return render(request, 'films/film_delete.html', context)

@login_required
@user_passes_test(is_staff_user)
def toggle_film_status(request, id):
    """Toggle film status between draft and published"""
    film = get_object_or_404(Film, id=id)
    
    if film.status == 'draft':
        film.status = 'published'
        message = f'Film "{film.title}" published successfully.'
    else:
        film.status = 'draft'
        message = f'Film "{film.title}" moved to draft.'
    
    film.save()
    messages.success(request, message)
    
    return redirect('films:film_management')

@login_required
@user_passes_test(is_staff_user)
def toggle_film_featured(request, id):
    """Toggle film featured status"""
    film = get_object_or_404(Film, id=id)
    
    film.featured = not film.featured
    film.save()
    
    status = "featured" if film.featured else "unfeatured"
    messages.success(request, f'Film "{film.title}" {status} successfully.')
    
    return redirect('films:film_management')

# Genre Management Views
@login_required
@user_passes_test(is_staff_user)
def genre_management(request):
    """Genre management page"""
    genres = Genre.objects.annotate(film_count=Count('films')).order_by('name')
    
    context = {
        'genres': genres,
        'total_genres': genres.count(),
    }
    return render(request, 'dashboard/modern_genre_management.html', context)

@login_required
@user_passes_test(is_staff_user)
def genre_create(request):
    """Create new genre"""
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            genre = form.save()
            messages.success(request, f'Genre "{genre.name}" created successfully.')
            return redirect('films:genre_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = GenreForm()
    
    context = {
        'form': form,
        'title': 'Create New Genre',
        'action': 'Create'
    }
    return render(request, 'dashboard/modern_genre_form.html', context)

@login_required
@user_passes_test(is_staff_user)
def genre_edit(request, id):
    """Edit existing genre"""
    genre = get_object_or_404(Genre, id=id)
    
    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            genre = form.save()
            messages.success(request, f'Genre "{genre.name}" updated successfully.')
            return redirect('films:genre_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = GenreForm(instance=genre)
    
    context = {
        'form': form,
        'genre': genre,
        'title': f'Edit Genre: {genre.name}',
        'action': 'Update'
    }
    return render(request, 'dashboard/modern_genre_form.html', context)

@login_required
@user_passes_test(is_staff_user)
@require_POST
def genre_delete(request, id):
    """Delete genre"""
    genre = get_object_or_404(Genre, id=id)
    genre_name = genre.name
    
    # Check if genre has films
    if genre.films.exists():
        messages.error(request, f'Cannot delete genre "{genre_name}" because it has films associated with it.')
    else:
        genre.delete()
        messages.success(request, f'Genre "{genre_name}" deleted successfully.')
    
    return redirect('films:genre_management')

def streaming_home(request):
    """Netflix-style streaming homepage for public"""
    # Featured films
    featured_films = Film.objects.filter(status='published', featured=True)[:6]
    featured_film = featured_films.first() if featured_films else None
    
    # Popular films (by review count)
    popular_films = Film.objects.filter(status='published').annotate(
        review_count=Count('reviews')
    ).order_by('-review_count')[:12]
    
    # Recent films
    recent_films = Film.objects.filter(status='published').order_by('-created_at')[:12]
    
    # Films by genre
    genres_with_films = []
    for genre in Genre.objects.all()[:5]:
        films = Film.objects.filter(status='published', genres=genre)[:8]
        if films:
            genres_with_films.append({
                'genre': genre,
                'films': films
            })
    
    context = {
        'featured_film': featured_film,
        'featured_films': featured_films,
        'popular_films': popular_films,
        'recent_films': recent_films,
        'genres_with_films': genres_with_films,
    }
    return render(request, 'films/public_streaming_home.html', context)

def watch_film(request, slug):
    """Watch film page with video player"""
    film = get_object_or_404(Film, slug=slug, status='published')
    
    # Get recommended films
    recommended_films = Film.objects.filter(
        status='published',
        genres__in=film.genres.all()
    ).exclude(id=film.id).distinct()[:6]
    
    context = {
        'film': film,
        'recommended_films': recommended_films,
    }
    return render(request, 'films/watch_film.html', context)

@login_required
def watchlist(request):
    """User's watchlist"""
    # For now, we'll use a simple approach with session-based watchlist
    # In production, you might want a proper Watchlist model
    watchlist_ids = request.session.get('watchlist', [])
    films = Film.objects.filter(id__in=watchlist_ids, status='published')
    
    context = {
        'films': films,
        'watchlist_count': len(watchlist_ids),
    }
    return render(request, 'films/watchlist.html', context)

@login_required
@require_POST
@csrf_exempt
def toggle_watchlist(request):
    """Add/remove film from watchlist"""
    film_id = request.POST.get('film_id')
    if not film_id:
        return JsonResponse({'error': 'Film ID required'}, status=400)
    
    try:
        film = Film.objects.get(id=film_id, status='published')
    except Film.DoesNotExist:
        return JsonResponse({'error': 'Film not found'}, status=404)
    
    watchlist = request.session.get('watchlist', [])
    
    if film_id in watchlist:
        watchlist.remove(film_id)
        in_watchlist = False
        message = f'"{film.title}" removed from watchlist'
    else:
        watchlist.append(film_id)
        in_watchlist = True
        message = f'"{film.title}" added to watchlist'
    
    request.session['watchlist'] = watchlist
    request.session.modified = True
    
    return JsonResponse({
        'in_watchlist': in_watchlist,
        'message': message,
        'watchlist_count': len(watchlist)
    })

def search_films(request):
    """Advanced film search page"""
    films = Film.objects.filter(status='published')
    genres = Genre.objects.all()
    
    # Search parameters
    query = request.GET.get('q', '')
    genre_id = request.GET.get('genre', '')
    rating = request.GET.get('rating', '')
    year = request.GET.get('year', '')
    sort_by = request.GET.get('sort', '-created_at')
    
    # Apply filters
    if query:
        films = films.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(director__icontains=query) |
            Q(cast__icontains=query)
        )
    
    if genre_id:
        films = films.filter(genres__id=genre_id)
    
    if rating:
        films = films.filter(rating=rating)
    
    if year:
        films = films.filter(release_date__year=year)
    
    films = films.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(films, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'genres': genres,
        'search_params': {
            'q': query,
            'genre': genre_id,
            'rating': rating,
            'year': year,
            'sort': sort_by,
        },
        'total_results': films.count(),
    }
    return render(request, 'films/search_results.html', context)

@login_required
@user_passes_test(is_staff_user)
@require_POST
def upload_video_ajax(request):
    """Handle AJAX video upload"""
    if 'video' not in request.FILES:
        return JsonResponse({'error': 'No video file provided'}, status=400)
    
    video_file = request.FILES['video']
    
    # Validate file size (max 500MB)
    max_size = 500 * 1024 * 1024  # 500MB
    if video_file.size > max_size:
        return JsonResponse({'error': 'File too large. Maximum size is 500MB.'}, status=400)
    
    # Validate file type
    allowed_types = ['video/mp4', 'video/avi', 'video/mov', 'video/wmv', 'video/flv']
    if video_file.content_type not in allowed_types:
        return JsonResponse({'error': 'Invalid file type. Only video files are allowed.'}, status=400)
    
    try:
        # Save file to temporary location
        file_path = default_storage.save(f'films/temp/{video_file.name}', video_file)
        
        return JsonResponse({
            'success': True,
            'file_path': file_path,
            'file_name': video_file.name,
            'file_size': video_file.size,
            'message': 'Video uploaded successfully!'
        })
    
    except Exception as e:
        return JsonResponse({'error': f'Upload failed: {str(e)}'}, status=500)

@login_required
@user_passes_test(is_staff_user)
@require_POST
def upload_image_ajax(request):
    """Handle AJAX image upload"""
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image file provided'}, status=400)
    
    image_file = request.FILES['image']
    
    # Validate file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    if image_file.size > max_size:
        return JsonResponse({'error': 'File too large. Maximum size is 10MB.'}, status=400)
    
    # Validate file type
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
    if image_file.content_type not in allowed_types:
        return JsonResponse({'error': 'Invalid file type. Only image files are allowed.'}, status=400)
    
    try:
        # Save file to temporary location
        upload_dir = request.POST.get('upload_type', 'poster')  # poster, backdrop, thumbnail
        file_path = default_storage.save(f'film_{upload_dir}s/temp/{image_file.name}', image_file)
        
        return JsonResponse({
            'success': True,
            'file_path': file_path,
            'file_name': image_file.name,
            'file_size': image_file.size,
            'preview_url': default_storage.url(file_path),
            'message': 'Image uploaded successfully!'
        })
    
    except Exception as e:
        return JsonResponse({'error': f'Upload failed: {str(e)}'}, status=500)
