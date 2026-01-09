# LibraryProject

 # My First Django Blog

A simple blog application built while learning Django framework  
(Perfect for Django beginners!)

## What is this project?

Super basic blog where you can:
- View all posts
- Read individual blog posts
- See posts by category (very simple version)
- Admin panel to add/edit/delete posts (of course! 🐍)

## Tech Stack

- Python 3.10+
- Django 4.2 / 5.0
- SQLite (default database - perfect for learning!)
- HTML + very little CSS (you can make it pretty later)

## Quick Start (5 minutes setup)

```bash
# 1. Clone or download the project
git clone https://github.com/yourusername/my-first-django-blog.git
cd my-first-django-blog

# 2. Create & activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

# 3. Install requirements
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create superuser (admin account)
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver