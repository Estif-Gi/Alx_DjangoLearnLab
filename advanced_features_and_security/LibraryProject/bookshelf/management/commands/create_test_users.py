from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book, CustomUser

class Command(BaseCommand):
    help = 'Creates test users and assigns them to appropriate groups'

    def handle(self, *args, **options):
        # Create or get groups
        viewer_group, _ = Group.objects.get_or_create(name='Viewers')
        editor_group, _ = Group.objects.get_or_create(name='Editors')
        admin_group, _ = Group.objects.get_or_create(name='Admins')

        # Create test users
        users_data = [
            {'username': 'viewer', 'email': 'viewer@example.com', 'password': 'viewerpass123', 'groups': [viewer_group]},
            {'username': 'editor', 'email': 'editor@example.com', 'password': 'editorpass123', 'groups': [editor_group]},
            {'username': 'admin', 'email': 'admin@example.com', 'password': 'adminpass123', 'groups': [admin_group]},
        ]

        for user_data in users_data:
            # Delete user if exists
            CustomUser.objects.filter(email=user_data['email']).delete()
            
            # Create user
            user = CustomUser.objects.create_user(
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['username'].capitalize(),
                last_name='User'
            )
            
            # Add user to groups
            for group in user_data['groups']:
                user.groups.add(group)
            
            self.stdout.write(self.style.SUCCESS(f'Successfully created user: {user.email}'))
            self.stdout.write(f'  - Password: {user_data["password"]}')
            self.stdout.write(f'  - Groups: {[g.name for g in user.groups.all()]}')
            self.stdout.write('---')

        self.stdout.write(self.style.SUCCESS('\nTest users created successfully!'))
