from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def create_groups_and_permissions(apps, schema_editor):
    # Get or create content type for Book model
    Book = apps.get_model('bookshelf', 'Book')
    content_type = ContentType.objects.get_for_model(Book)
    
    # Create groups
    viewers_group, _ = Group.objects.get_or_create(name='Viewers')
    editors_group, _ = Group.objects.get_or_create(name='Editors')
    admins_group, _ = Group.objects.get_or_create(name='Admins')
    
    # Get or create permissions
    view_perm, _ = Permission.objects.get_or_create(
        codename='can_view_book',
        content_type=content_type,
        defaults={'name': 'Can view book details'}
    )
    
    create_perm, _ = Permission.objects.get_or_create(
        codename='can_create_book',
        content_type=content_type,
        defaults={'name': 'Can create book entries'}
    )
    
    edit_perm, _ = Permission.objects.get_or_create(
        codename='can_edit_book',
        content_type=content_type,
        defaults={'name': 'Can edit books'}
    )
    
    delete_perm, _ = Permission.objects.get_or_create(
        codename='can_delete_book',
        content_type=content_type,
        defaults={'name': 'Can delete books'}
    )
    
    # Assign permissions to groups
    viewers_group.permissions.set([view_perm])
    editors_group.permissions.set([view_perm, create_perm, edit_perm])
    admins_group.permissions.set([view_perm, create_perm, edit_perm, delete_perm])


def reverse_func(apps, schema_editor):
    # This function will delete the groups when unapplying the migration
    Group.objects.filter(name__in=['Viewers', 'Editors', 'Admins']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('bookshelf', '0002_book_date_of_birth_book_profile_photo_customuser'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions, reverse_func),
    ]
