from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    summary =models.TextField(max_length=1000, help_text='Enter a brief decription about a book')
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Characters <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a> ')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    language_choices = (
        ('English', 'English'),
        ('Farsi', 'Farsi')
        )

    language = models.CharField(max_length=7,choices=language_choices, default='English')

    def __str__(self):
        return self.title

    def display_genre(self):
        return ','.join(genre.name for genre in self.genre.all()[:2])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back )

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, default='m', blank=True, help_text='Book availability')

    class Meta:
        ordering = ['due_back']
    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),)
    
    def __str__(self):
        return f'{self.id}({self.book}'

class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.DateField(blank=False, null=True)
    date_of_death = models.DateField('died',blank=True, null=True)

    class Meta:
        ordering = ['first_name','last_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name},{self.first_name}'