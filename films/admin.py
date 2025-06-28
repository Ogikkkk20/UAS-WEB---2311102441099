from django.contrib import admin
from django.utils.html import format_html
from .models import Genre, Film, FilmReview

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'film_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

    def film_count(self, obj):
        return obj.films.count()
    film_count.short_description = 'Films'

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ['title', 'director', 'status', 'rating', 'featured', 'views_count', 'created_at']
    list_filter = ['status', 'rating', 'featured', 'genres', 'created_at']
    search_fields = ['title', 'director', 'cast', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['genres']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    date_hierarchy = 'release_date'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'synopsis')
        }),
        ('Media', {
            'fields': ('poster', 'trailer_url')
        }),
        ('Film Details', {
            'fields': ('director', 'cast', 'genres', 'release_date', 'duration', 'rating', 'imdb_rating')
        }),
        ('Status & Management', {
            'fields': ('status', 'featured', 'created_by')
        }),
        ('Statistics', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new film
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(FilmReview)
class FilmReviewAdmin(admin.ModelAdmin):
    list_display = ['film', 'user', 'rating', 'approved', 'created_at']
    list_filter = ['rating', 'approved', 'created_at']
    search_fields = ['film__title', 'user__username', 'title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['approve_reviews', 'unapprove_reviews']

    def approve_reviews(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f'{updated} reviews were approved.')
    approve_reviews.short_description = 'Approve selected reviews'

    def unapprove_reviews(self, request, queryset):
        updated = queryset.update(approved=False)
        self.message_user(request, f'{updated} reviews were unapproved.')
    unapprove_reviews.short_description = 'Unapprove selected reviews'
