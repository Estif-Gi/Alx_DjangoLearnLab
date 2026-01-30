from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .models import Book

# Function-based views with permission decorators

@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    """View for listing all books"""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_detail(request, pk):
    """View for displaying a single book's details"""
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create(request):
    """View for creating a new book"""
    if request.method == 'POST':
        # In a real implementation, you would use a form here
        title = request.POST.get('title')
        author = request.POST.get('author')
        # ... handle other fields
        
        book = Book.objects.create(
            title=title,
            author=author,
            # ... set other fields
        )
        messages.success(request, 'Book created successfully!')
        return redirect('book_detail', pk=book.pk)
    
    return render(request, 'bookshelf/book_form.html', {'form_title': 'Create Book'})

@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def book_update(request, pk):
    """View for updating an existing book"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        # In a real implementation, you would use a form here
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        # ... update other fields
        book.save()
        messages.success(request, 'Book updated successfully!')
        return redirect('book_detail', pk=book.pk)
    
    return render(request, 'bookshelf/book_form.html', {
        'form_title': 'Update Book',
        'book': book
    })

@login_required
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def book_delete(request, pk):
    """View for deleting a book"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# Class-based views with permission mixins

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('bookshelf.can_view_book', raise_exception=True), name='dispatch')
class BookListView(ListView):
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('bookshelf.can_view_book', raise_exception=True), name='dispatch')
class BookDetailView(DetailView):
    model = Book
    template_name = 'bookshelf/book_detail.html'
    context_object_name = 'book'

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('bookshelf.can_create_book', raise_exception=True), name='dispatch')
class BookCreateView(CreateView):
    model = Book
    template_name = 'bookshelf/book_form.html'
    fields = ['title', 'author', 'publication_year']
    success_url = reverse_lazy('book_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Book created successfully!')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('bookshelf.can_edit_book', raise_exception=True), name='dispatch')
class BookUpdateView(UpdateView):
    model = Book
    template_name = 'bookshelf/book_form.html'
    fields = ['title', 'author', 'publication_year']
    
    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Book updated successfully!')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('bookshelf.can_delete_book', raise_exception=True), name='dispatch')
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'bookshelf/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Book deleted successfully!')
        return super().delete(request, *args, **kwargs)
