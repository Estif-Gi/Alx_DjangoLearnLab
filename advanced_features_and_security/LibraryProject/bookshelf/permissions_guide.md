# Django Permission System Guide

This document explains the permission system implemented in the Library Management application.

## Permission Structure

The system implements a role-based access control (RBAC) system with the following permissions for the Book model:

- `can_view_book`: View book details
- `can_create_book`: Create new book entries
- `can_edit_book`: Edit existing books
- `can_delete_book`: Delete books

## User Groups

Three user groups have been created with the following permissions:

### 1. Viewers
- Can view book details

### 2. Editors
- Can view book details
- Can create new book entries
- Can edit existing books

### 3. Admins
- Can view book details
- Can create new book entries
- Can edit existing books
- Can delete books

## Implementation Details

### Models
- Custom permissions are defined in the `Book` model's `Meta` class
- The `CustomUser` model extends Django's `AbstractUser` for authentication

### Admin Interface
- The admin interface has been customized to respect the permission system
- Users will only see options they have permission to access
- The Group admin interface shows the number of permissions assigned to each group

### Views
All views should be protected with the appropriate permission decorators:

```python
from django.contrib.auth.decorators import permission_required

@permission_required('bookshelf.can_view_book')
def book_list(request):
    # View implementation
    pass

@permission_required('bookshelf.can_create_book')
def book_create(request):
    # View implementation
    pass
```

## Testing the Permission System

1. Create test users and assign them to different groups
2. Log in as each user and verify they can only perform allowed actions
3. Check that the admin interface shows/hides options based on permissions

## Adding New Permissions

To add new permissions:

1. Add the permission to the model's `Meta` class
2. Create and run a new migration
3. Update the group permissions as needed
4. Update the views to check for the new permissions

## Best Practices

- Always use permission decorators or mixins to protect views
- Test permissions thoroughly after any changes
- Document any custom permissions and their intended use
- Consider using Django's built-in permission mixins for class-based views
