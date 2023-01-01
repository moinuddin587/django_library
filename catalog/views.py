from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import BookRenewForm
import datetime
from django.urls import reverse_lazy, reverse

def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_authors = Author.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_authors': num_authors,
        'num_instances_available': num_instances_available,
        'num_visits': num_visits
    }
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 3


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 7


class AuthorDetailView(generic.DetailView):
    model = Author

class BorrowedBookByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

#this is the challenge
class DisplayToLibrarianListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowedbook.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o')

@login_required
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = BookRenewForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            
            return HttpResponseRedirect(reverse('borrowed-books'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = BookRenewForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreateView(CreateView):
    model = Author
    fields = '__all__'

class AuthorUpdateView(UpdateView):
    model =Author
    fields = '__all__'

class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')