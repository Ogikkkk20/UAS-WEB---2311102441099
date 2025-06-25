# forms.py
from django import forms
from .models import Kategori

class KategoriForm(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = ['nama']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Kategori'}),
        }
