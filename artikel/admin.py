from django.contrib import admin
from artikel.models import *
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'created_by']
    search_fields = ['name']

class PostAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'created_at', 'author']
    search_fields = ['category__name', 'title']

class CommentPost(admin.ModelAdmin):
    list_display = ['name', 'content']
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentPost)
