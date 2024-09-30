from django import forms
from .models import Book, Author

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']  # Corrected 'feilds' to 'fields'
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':"Enter the author's name"}),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'  # Corrected 'feilds' to 'fields'
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the books name'}),
            'author':forms.Select(attrs={'class':'form-control','placeholder':'Enter the books name'}),
            'price':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter the books name'}),

        }

