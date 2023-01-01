from django.test import TestCase
from django.contrib.auth.models import User
from catalog.models import Author, Book, BookInstance, Genre
from django.urls import reverse
from django.utils import timezone
import datetime


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(first_name=f"Dominique {author_id}",last_name=f"Surname {author_id}")

    def test_url_is_on_correct_destination(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_view_is_paginated(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']), 7)

    def test_all_author_list(self):
        response = self.client.get(reverse('authors')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 6)

class BookListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        list_of_books = 10
        for book_id in range(list_of_books):
            Book.objects.create(title=f"Book {book_id}")

    def test_book_url(self):
        response = self.client.get('/catalog/books/')
        self.assertEqual(response.status_code, 200)

    def test_url_by_name(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='catalog/book_list.html')

    def test_paginated(self):
        response = self.client.get('/catalog/books/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['book_list']), 3)

    def test_paginated_page_two(self):
        response = self.client.get('/catalog/books/'+'?page=4')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['book_list']), 1)

class BorrowedBookByUserListViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username="raihan", password="chy@657252")
        test_user2 = User.objects.create_user(username="rafsan", password="chy@657252" )

        test_user1.save()
        test_user2.save()

        test_isbn = "123457585"
        test_summary = "A book of tales"
        test_genre = Genre.objects.create(name="Fiction")
        test_author = Author.objects.create(first_name="Omar", last_name="Haider")
        test_language= "English"

        test_book =Book.objects.create(
            title = "Harry Potter",
            isbn = test_isbn,
            summary = test_summary,
            author = test_author,
            language = test_language
        )

        genre_for_all_books = Genre.objects.all()
        test_book.genre.set(genre_for_all_books)
        test_book.save()

        book_copies = 30
        for book_copy in range(book_copies):
            return_date = timezone.localtime() + datetime.timedelta(days=book_copy%5)
            the_borrower = test_user1 if book_copy % 2 else test_user2
            BookInstance.objects.create(
                imprint = "Version 2.0, 2022",
                status = "m",
                due_back = return_date,
                borrower = the_borrower,
                book = test_book
            )
    def test_user_not_logged_in(self):
        response = self.client.get(reverse('my_borrowed'))
        self.assertRedirects(response, '/accounts/login/?next=/catalog/my_books/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='raihan', password='chy@657252')
        response = self.client.get(reverse('my_borrowed'))

        self.assertEqual(str(response.context['user']), 'raihan')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'catalog/bookinstance_list_borrowed_user.html')

    def test_only_borrowed_books_in_list(self):
        login = self.client.login(username='raihan',password='chy@657252')
        response = self.client.get(reverse('my_borrowed'))

        self.assertEqual(str(response.context['user']), 'raihan')
        self.assertEqual(response.status_code, 200)

        self.assertTrue('bookinstance_list' in response.context)
        self.assertEqual(len(response.context['bookinstance_list']), 0)

        books = BookInstance.objects.all()[:10]

        for book in books:
            book.status = 'o'
            book.save()

        
        login = self.client.login(username='raihan', password='chy@657252')
        response = self.client.get(reverse('my_borrowed'))

        self.assertEqual(len(response.context['bookinstance_list']), 0)


    def test_pages_ordered_by_due_date(self):
        # Change all books to be on loan
        for book in BookInstance.objects.all():
            book.status='o'
            book.save()

        login = self.client.login(username='raihan', password='chy@657252')
        response = self.client.get(reverse('my_borrowed'))


        # Confirm that of the items, only 10 are displayed due to pagination.
        self.assertEqual(len(response.context['bookinstance_list']), 10)    
        
























