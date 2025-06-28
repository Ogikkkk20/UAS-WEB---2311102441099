from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django import forms
import json

# Custom User Form for Admin
class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False, 
                              help_text="Leave blank to keep current password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(), required=False,
                                     help_text="Confirm password")
    
    # Add custom fields that aren't in User model
    GENDER_CHOICES = [
        ('', 'Select Gender'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False,
                              widget=forms.Select(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=15, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'User bio'}), 
                         required=False)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Handle password
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        
        if password:
            if password != password_confirm:
                raise forms.ValidationError("Passwords don't match")
            user.set_password(password)
        
        if commit:
            user.save()
            # Note: gender, phone, bio are form fields but not saved to User model
            # In a real app, you'd save these to a UserProfile model
        
        return user

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                              help_text="Enter a strong password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                     help_text="Confirm password")
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'checked': True}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password != password_confirm:
            raise forms.ValidationError("Passwords don't match")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

def is_admin_or_staff(user):
    """Check if user is admin or staff"""
    return user.is_authenticated and (user.is_superuser or user.is_staff)

@login_required
@user_passes_test(is_admin_or_staff)
def user_management(request):
    """User management page"""
    # Search functionality
    search_query = request.GET.get('search', '')
    user_type = request.GET.get('type', 'all')
    
    # Base queryset
    users = User.objects.all().order_by('-date_joined')
    
    # Apply search filter
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Apply type filter
    if user_type == 'admin':
        users = users.filter(is_superuser=True)
    elif user_type == 'staff':
        users = users.filter(is_staff=True, is_superuser=False)
    elif user_type == 'regular':
        users = users.filter(is_staff=False, is_superuser=False)
    
    # Pagination
    paginator = Paginator(users, 15)  # Show 15 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    stats = {
        'total': User.objects.count(),
        'admin': User.objects.filter(is_superuser=True).count(),
        'staff': User.objects.filter(is_staff=True, is_superuser=False).count(),
        'regular': User.objects.filter(is_staff=False, is_superuser=False).count(),
        'active': User.objects.filter(is_active=True).count(),
        'inactive': User.objects.filter(is_active=False).count(),
    }
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'user_type': user_type,
        'stats': stats,
    }
    
    return render(request, 'dashboard/modern_user_management.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
def user_detail(request, user_id):
    """User detail page"""
    user = get_object_or_404(User, id=user_id)
    
    context = {
        'user_detail': user,
    }
    
    return render(request, 'user_detail.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
def toggle_user_status(request, user_id):
    """Toggle user active status via AJAX"""
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        
        # Prevent disabling self
        if user == request.user:
            return JsonResponse({
                'success': False, 
                'message': 'You cannot disable your own account'
            })
        
        # Toggle status
        user.is_active = not user.is_active
        user.save()
        
        status = 'activated' if user.is_active else 'deactivated'
        
        return JsonResponse({
            'success': True,
            'message': f'User {user.username} has been {status}',
            'is_active': user.is_active
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
@user_passes_test(is_admin_or_staff)
def delete_user(request, user_id):
    """Delete user"""
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        
        # Prevent deleting self
        if user == request.user:
            messages.error(request, 'You cannot delete your own account')
            return redirect('user_management')
        
        username = user.username
        user.delete()
        messages.success(request, f'User {username} has been deleted successfully')
        
        return redirect('user_management')
    
    return redirect('user_management')

@login_required
def user_list_api(request):
    """API endpoint for user list (JSON)"""
    users = User.objects.all().order_by('-date_joined')
    
    user_data = []
    for user in users:
        user_data.append({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
            'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else 'Never'
        })
    
    return JsonResponse({
        'users': user_data,
        'total': len(user_data)
    })

@login_required
@user_passes_test(is_admin_or_staff)
def user_create(request):
    """Create new user"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} has been created successfully')
            return redirect('user_management')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form,
        'title': 'Create New User',
        'action': 'Create'
    }
    
    return render(request, 'dashboard/modern_user_form.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
def user_edit(request, user_id):
    """Edit existing user"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            messages.success(request, f'User {user.username} has been updated successfully')
            return redirect('user_management')
    else:
        form = CustomUserForm(instance=user)
    
    context = {
        'form': form,
        'user_obj': user,
        'title': f'Edit User: {user.username}',
        'action': 'Update'
    }
    
    return render(request, 'dashboard/modern_user_form.html', context)
