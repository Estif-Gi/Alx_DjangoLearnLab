from django.contrib import admin
from .models import Book

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year',)
    search_fields = ('title', 'author')


class CustomUserAdmin(BaseUserAdmin):
    # [keep all the existing CustomUserAdmin code]
    ...

# Add these lines at the bottom of the file:
admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser, CustomUserAdmin)