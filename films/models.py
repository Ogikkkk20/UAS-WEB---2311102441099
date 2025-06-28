from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Genre(models.Model):
    """Model untuk genre film"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Film(models.Model):
    """Model untuk film"""
    RATING_CHOICES = [
        ('G', 'General Audiences'),
        ('PG', 'Parental Guidance'),
        ('PG-13', 'Parents Strongly Cautioned'),
        ('R', 'Restricted'),
        ('NC-17', 'Adults Only'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    synopsis = models.TextField(help_text="Detailed synopsis of the film")
    
    # Media
    poster = models.ImageField(upload_to='film_posters/', blank=True, null=True)
    backdrop = models.ImageField(upload_to='film_backdrops/', blank=True, null=True, help_text="Large banner image for film")
    trailer_url = models.URLField(blank=True, help_text="YouTube or other trailer video URL")
    video_file = models.FileField(upload_to='films/', blank=True, null=True, help_text="Main film video file")
    video_url = models.URLField(blank=True, help_text="External video URL (YouTube, Vimeo, etc.)")
    thumbnail = models.ImageField(upload_to='film_thumbnails/', blank=True, null=True, help_text="Video thumbnail")
    
    # Details
    director = models.CharField(max_length=200)
    cast = models.TextField(help_text="Main cast members, separated by commas")
    genres = models.ManyToManyField(Genre, related_name='films')
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, default='PG')
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    
    # Status and Management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False, help_text="Show in featured section")
    views_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='films')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('film_detail', kwargs={'slug': self.slug})

    def get_cast_list(self):
        """Return cast as a list"""
        return [name.strip() for name in self.cast.split(',') if name.strip()]

    def get_genre_names(self):
        """Return genre names as string"""
        return ", ".join([genre.name for genre in self.genres.all()])

    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['featured', '-created_at']),
        ]

class FilmReview(models.Model):
    """Model untuk review film"""
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.film.title} - {self.rating}/5 by {self.user.username}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ['film', 'user']  # One review per user per film
