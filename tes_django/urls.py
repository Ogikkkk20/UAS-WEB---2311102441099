from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.views.generic import RedirectView

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from tes_django.views import * 
from tes_django.authentication import login, registrasi, logout
from tes_django.database_views import database_view
from tes_django.user_views import user_management, user_detail, toggle_user_status, delete_user, user_list_api, user_create, user_edit
from tes_django.analytics_views import analytics
from films import views as films_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication routes
    path('login/', login, name='login'),
    path('registrasi/', registrasi, name='registrasi'),
    path('logout/', logout, name='logout'),
    
    # Legacy dashboard routes
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/articles/', include('artikel.urls')),
    
    # Database View
    path('database/', database_view, name='database_view'),
    
    # User Management
    path('users/management/', user_management, name='user_management'),
    path('users/create/', user_create, name='user_create'),
    path('users/<int:user_id>/edit/', user_edit, name='user_edit'),
    path('users/<int:user_id>/', user_detail, name='user_detail'),
    path('users/<int:user_id>/toggle-status/', toggle_user_status, name='toggle_user_status'),
    path('users/<int:user_id>/delete/', delete_user, name='delete_user'),
    path('api/users/', user_list_api, name='user_list_api'),
    
    # Legacy routes
    path('article_detail/<int:id>/', article_detail, name='article_detail'),
    path('cv/', cv, name='cv'),
    path('rate/', rate, name='rate'),
    
    # Films app routes
    path('films/', include('films.urls')),
    
    # Quick access shortcuts
    path('management/', RedirectView.as_view(url='/films/management/', permanent=False), name='management_redirect'),
    
    # Homepage - redirect to films streaming
    path('', RedirectView.as_view(url='/films/', permanent=False), name='home'),
    
    # Analytics
    path('analytics/', analytics, name='analytics'),
]

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)