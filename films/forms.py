from django import forms
from django.contrib.auth.models import User
from .models import Film, Genre, FilmReview

class FilmForm(forms.ModelForm):
    """Form untuk create/edit film dengan CKEditor"""
    
    # Hidden fields for AJAX uploaded files
    video_path = forms.CharField(required=False, widget=forms.HiddenInput())
    poster_path = forms.CharField(required=False, widget=forms.HiddenInput())
    
    class Meta:
        model = Film
        fields = [
            'title', 'description', 'synopsis', 'poster', 'backdrop', 'thumbnail',
            'trailer_url', 'video_file', 'video_url', 'director', 'cast', 'genres', 
            'release_date', 'duration', 'rating', 'imdb_rating', 'status', 'featured'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter film title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Short description of the film',
                'required': True
            }),
            'synopsis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Detailed synopsis of the film'
            }),
            'poster': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'backdrop': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'trailer_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://youtube.com/watch?v=...'
            }),
            'video_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://youtube.com/embed/... or external video URL'
            }),
            'director': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Director name'
            }),
            'cast': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Main cast members, separated by commas'
            }),
            'genres': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'release_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duration in minutes'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select'
            }),
            'imdb_rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'max': '10',
                'placeholder': 'e.g., 8.5'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make some fields required
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['director'].required = True
        self.fields['release_date'].required = True
        self.fields['duration'].required = True

class GenreForm(forms.ModelForm):
    """Form untuk create/edit genre"""
    
    class Meta:
        model = Genre
        fields = ['name', 'description']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Genre name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control ckeditor',
                'rows': 3,
                'placeholder': 'Genre description'
            }),
        }

class FilmReviewForm(forms.ModelForm):
    """Form untuk user review"""
    
    class Meta:
        model = FilmReview
        fields = ['rating', 'title', 'content']
        
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-select'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Review title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control ckeditor',
                'rows': 6,
                'placeholder': 'Write your review here...'
            }),
        }

class FilmSearchForm(forms.Form):
    """Form untuk search dan filter film"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search films...'
        })
    )
    
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        empty_label="All Genres",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    rating = forms.ChoiceField(
        choices=[('', 'All Ratings')] + Film.RATING_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Film.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    sort_by = forms.ChoiceField(
        choices=[
            ('-created_at', 'Newest First'),
            ('created_at', 'Oldest First'),
            ('title', 'Title A-Z'),
            ('-title', 'Title Z-A'),
            ('-views_count', 'Most Popular'),
            ('-imdb_rating', 'Highest Rated'),
        ],
        required=False,
        initial='-created_at',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
