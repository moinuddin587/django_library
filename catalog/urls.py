from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('my_books/', views.BorrowedBookByUserListView.as_view(), name='my_borrowed'),
    path('borrowed_books/', views.DisplayToLibrarianListView.as_view(), name='borrowed-books'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create', views.AuthorCreateView.as_view(), name='author-create'),
    path('author/<int:pk>/update', views.AuthorUpdateView.as_view(), name='author-update'),
    path('author/<int:pk>/delete', views.AuthorDeleteView.as_view(), name='author-delete'),
]