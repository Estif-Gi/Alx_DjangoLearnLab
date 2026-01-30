from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    # Book views
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/new/', views.book_create, name='book_create'),
    path('book/<int:pk>/edit/', views.book_update, name='book_update'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
    
    # Example contact form
    path('contact/', views.example_contact, name='example_contact'),
]
