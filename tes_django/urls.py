from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from tes_django.views import * 
from tes_django.authentication import login, registrasi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome, name='home'),
    path('article_detail/<int:id>', article_detail, name='article_detail'),
    path('cv/', cv, name='cv'),
    path('rate/', rate, name='rate'),

    path('dashboard', dashboard, name='dashboard'),

    path('dashboard/', include('artikel.urls')),

    ###################### Authentication ######################
    
    path('login', login, name='login'),
    path('registrasi', registrasi, name='registrasi'),
]

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)