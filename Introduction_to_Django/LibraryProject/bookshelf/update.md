from bookshelf.models import Book

# Retrieve and update
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Check updated title
book.title

# Expected Output:
# 'Nineteen Eighty-Four'
