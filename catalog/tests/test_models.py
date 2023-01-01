from django.test import TestCase
from catalog.models import Author, Genre, Book

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Raihan', last_name='Chy')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_death_of_death(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'died')


    def test_return_first_name_comma_last_name(self):
        author =Author.objects.get(id=1)
        returend_name = f"{author.last_name},{author.first_name}"
        self.assertEqual(str(author), returend_name)

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1/')

class GenreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name='comics')

    def test_genre_name_label(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_genre_name_max_length(self):
        genre = Genre.objects.get(id=1)
        length = genre._meta.get_field('name').max_length
        self.assertEqual(length, 200)

    def test_return_name(self):
        genre = Genre.objects.get(id=1)
        self.assertEqual(str(genre), genre.name)

class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Book.objects.create(title='Harry Potter')

    def test_return_title(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label,'title')
    
    def test_summary_length(self):
        book=Book.objects.get(id=1)
        summary_length = book._meta.get_field('summary').max_length
        self.assertEqual(summary_length, 1000)
    
    def test_return_author(self):
        book= Book.objects.get(id=1)
        field_label = book._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_isbn_title(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('isbn').verbose_name
        self.assertEqual(field_label, 'ISBN')

    def test_return_string(self):
        book =Book.objects.get(id=1)
        self.assertEqual(str(book), 'Harry Potter')

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.get_absolute_url(), '/catalog/book/1/' )

