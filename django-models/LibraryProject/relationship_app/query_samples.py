import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def query_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return []

# List all books in a library
def query_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return []

# Retrieve the librarian for a library
def query_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None

# Example usage (assuming some data exists)
if __name__ == "__main__":
    # Assuming an author named 'J.K. Rowling' exists
    books = query_books_by_author('J.K. Rowling')
    print("Books by J.K. Rowling:", [book.title for book in books])

    # Assuming a library named 'Central Library' exists
    books_in_lib = query_books_in_library('Central Library')
    print("Books in Central Library:", [book.title for book in books_in_lib])

    # Assuming a librarian for 'Central Library'
    librarian = query_librarian_for_library('Central Library')
    if librarian:
        print("Librarian for Central Library:", librarian.name)
    else:
        print("No librarian found")