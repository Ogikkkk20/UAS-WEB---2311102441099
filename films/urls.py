from django.urls import path
from . import views

app_name = 'films'

urlpatterns = [
    # Streaming URLs
    path('', views.streaming_home, name='streaming_home'),
    path('browse/', views.film_list, name='film_list'),
    path('search/', views.search_films, name='search_films'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('toggle-watchlist/', views.toggle_watchlist, name='toggle_watchlist'),
    
    # Management URLs (Staff only) - MUST BE BEFORE <slug:slug>/
    path('management/', views.film_management, name='film_management'),
    path('management/create/', views.film_create, name='film_create'),
    path('management/edit/<int:id>/', views.film_edit, name='film_edit'),
    path('management/delete/<int:id>/', views.film_delete, name='film_delete'),
    path('management/toggle-status/<int:id>/', views.toggle_film_status, name='toggle_film_status'),
    path('management/toggle-featured/<int:id>/', views.toggle_film_featured, name='toggle_film_featured'),
    
    # AJAX Upload URLs
    path('ajax/upload-video/', views.upload_video_ajax, name='upload_video_ajax'),
    path('ajax/upload-image/', views.upload_image_ajax, name='upload_image_ajax'),
    
    # Genre Management
    path('management/genres/', views.genre_management, name='genre_management'),
    path('management/genres/create/', views.genre_create, name='genre_create'),
    path('management/genres/edit/<int:id>/', views.genre_edit, name='genre_edit'),
    path('management/genres/delete/<int:id>/', views.genre_delete, name='genre_delete'),
    
    # Film Detail and Streaming - MUST BE LAST (catch-all patterns)
    path('watch/<slug:slug>/', views.watch_film, name='watch_film'),
    path('<slug:slug>/review/', views.add_review, name='add_review'),
    path('<slug:slug>/', views.film_detail, name='film_detail'),
]
