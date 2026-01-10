from bookshelf.models import Book

# Retrieve and delete
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Check if any books remain
Book.objects.all()

# Expected Output:
# <QuerySet []>
