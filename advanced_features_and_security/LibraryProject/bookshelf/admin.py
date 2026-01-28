from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Book, CustomUser

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year',)
    search_fields = ('title', 'author')

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    
    # Make sure these fields are read-only for non-superusers
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('is_staff', 'is_superuser', 'groups', 'user_permissions')
        return super().get_readonly_fields(request, obj)
