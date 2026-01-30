from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Book
from .forms import BookForm, BookSearchForm
from .forms import ExampleForm

# Function-based views with permission decorators

@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    """
    View for listing books with search and filtering capabilities.
    Uses parameterized queries to prevent SQL injection.
    """
    form = BookSearchForm(request.GET or None)
    books = Book.objects.all()
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        year = form.cleaned_data.get('publication_year')
        sort_by = form.cleaned_data.get('sort_by', 'title_asc')
        
        # Safe search using Q objects and parameterized queries
        if query:
            books = books.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query)
            )
        
        # Safe filtering by year
        if year:
            books = books.filter(publication_year__year=year)
        
        # Safe sorting
        sort_mapping = {
            'title_asc': 'title',
            'title_desc': '-title',
            'author_asc': 'author',
            'author_desc': '-author',
            'year_asc': 'publication_year',
            'year_desc': '-publication_year',
        }
        books = books.order_by(sort_mapping.get(sort_by, 'title'))
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(books, 10)  # 10 items per page
    
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'form': form,
    })

@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_detail(request, pk):
    """View for displaying a single book's details"""
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create(request):
    """
    View for creating a new book.
    Uses ModelForm for safe data handling and validation.
    """
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            messages.success(request, 'Book created successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'form_title': 'Create Book'
    })

@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def book_update(request, pk):
    """
    View for updating an existing book.
    Uses ModelForm for safe data handling and validation.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            updated_book = form.save(commit=False)
            updated_book.updated_by = request.user
            updated_book.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
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

@login_required
def example_contact(request):
    """
    Example view demonstrating the use of ExampleForm.
    This could be used for a contact page or feedback form.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # In a real application, you would process the form data here
            # For example, send an email or save to the database
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_copy = form.cleaned_data.get('send_copy', False)
            
            # Process the form data (placeholder for actual implementation)
            print(f"Form submitted by {name} <{email}>: {message}")
            if send_copy:
                print("A copy was requested to be sent to the user.")
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('example_contact')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_contact.html', {'form': form})


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
