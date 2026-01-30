from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Book


class BookForm(forms.ModelForm):
    """Form for creating and updating Book instances."""
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'profile_photo']
        widgets = {
            'publication_year': forms.DateInput(attrs={'type': 'date'}),
            'profile_photo': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def clean_publication_year(self):
        """Validate that publication year is not in the future."""
        publication_year = self.cleaned_data.get('publication_year')
        if publication_year and publication_year > timezone.now().date():
            raise ValidationError("Publication year cannot be in the future.")
        return publication_year

    def clean_title(self):
        """Ensure title is not empty and has proper formatting."""
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError("Title cannot be empty.")
        return title


class ExampleForm(forms.Form):
    """Example form for demonstration purposes."""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter your message'
        })
    )
    send_copy = forms.BooleanField(
        required=False,
        initial=True,
        label='Send me a copy',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def clean(self):
        """Example of form-wide validation."""
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        message = cleaned_data.get('message')

        # Example validation: Check if name appears in message
        if name and message and name.lower() in message.lower():
            self.add_error('message', "Please don't include your name in the message.")

        return cleaned_data


class BookSearchForm(forms.Form):
    """Form for searching books."""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title or author...',
            'aria-label': 'Search'
        })
    )
    
    publication_year = forms.IntegerField(
        required=False,
        min_value=1000,
        max_value=timezone.now().year,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by year',
            'min': '1000',
            'max': str(timezone.now().year)
        })
    )
    
    SORT_CHOICES = [
        ('title_asc', 'Title (A-Z)'),
        ('title_desc', 'Title (Z-A)'),
        ('author_asc', 'Author (A-Z)'),
        ('author_desc', 'Author (Z-A)'),
        ('year_asc', 'Publication Year (Oldest First)'),
        ('year_desc', 'Publication Year (Newest First)'),
    ]
    
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
