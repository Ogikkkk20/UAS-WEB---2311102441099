from django.urls import path
from artikel.views import *
from . import views

urlpatterns = [
    path('kategori/list', views.admin_kategori_list, name="admin_kategori_list"),

]