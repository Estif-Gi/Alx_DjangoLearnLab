from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library

# Create your views here.

def list_books(request):
    books = Book.objects.all()
    response = "Books Available:\n"
    for book in books:
        response += f"{book.title} by {book.author.name}\n"
    return HttpResponse(response, content_type='text/plain')

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
