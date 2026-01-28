from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Book, CustomUser

def create_groups_and_permissions(apps, schema_editor):
    # Get or create content type for Book model
    content_type = ContentType.objects.get_for_model(Book)
    
    # Create groups
    viewers_group, _ = Group.objects.get_or_create(name='Viewers')
    editors_group, _ = Group.objects.get_or_create(name='Editors')
    admins_group, _ = Group.objects.get_or_create(name='Admins')
    
    # Get permissions
    view_perm = Permission.objects.get(codename='can_view_book', content_type=content_type)
    create_perm = Permission.objects.get(codename='can_create_book', content_type=content_type)
    edit_perm = Permission.objects.get(codename='can_edit_book', content_type=content_type)
    delete_perm = Permission.objects.get(codename='can_delete_book', content_type=content_type)
    
    # Assign permissions to groups
    viewers_group.permissions.set([view_perm])
    editors_group.permissions.set([view_perm, create_perm, edit_perm])
    admins_group.permissions.set([view_perm, create_perm, edit_perm, delete_perm])

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year',)
    search_fields = ('title', 'author')
    
    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('bookshelf.can_view_book')
    
    def has_add_permission(self, request):
        return request.user.has_perm('bookshelf.can_create_book')
    
    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('bookshelf.can_edit_book')
    
    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('bookshelf.can_delete_book')

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

# Unregister the default Group model and register our custom one
admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ['permissions']
    list_display = ('name', 'get_permissions_count')
    
    def get_permissions_count(self, obj):
        return obj.permissions.count()
    get_permissions_count.short_description = 'Number of Permissions'

# Create initial groups and permissions
# This would typically be done in a data migration
# For development, you can run this in the shell
# create_groups_and_permissions(None, None)