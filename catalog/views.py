from audioop import reverse
import datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm, ReturnBookModelForm
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
from .models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_fiction_genres = Genre.objects.filter(name__icontains='fiction').count()

    num_dragon_books = Book.objects.filter(title__icontains='dragon').count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_fiction_genres': num_fiction_genres,
        'num_dragon_books': num_dragon_books,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. (For staff)"""
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If a POST request, process Form data
    if request.method == 'POST':
            # Create a form instance and populate it with data from the request (binding):
            form = RenewBookForm(request.POST)

            # Check if form is valid
            if form.is_valid():
                # process data in form.cleaned_data as required (here we just write it to the model due_back field)
                book_instance.due_back = form.cleaned_data['renewal_date']
                book_instance.save()

                # redirect to a new URL:
                return HttpResponseRedirect(reverse('all-borrowed'))
    # if this is a GET request (or any other request) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

        context = {
            'form': form,
            'book_instance': book_instance,
        }

        return render(request, 'catalog/book_renew_librarian.html', context)

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def return_book_librarian(request, pk):
    """View function for returning a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # if POST, process data.
    if request.method == 'POST':
        form = ReturnBookModelForm(request.POST)

        if form.is_valid():
            book_instance.due_back = None
            book_instance.borrower = None
            book_instance.status = form.cleaned_data['status']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
    
    else:
        proposed_return_status = 'a'
        form = ReturnBookModelForm(initial={'status': proposed_return_status})

        context = {
            'form': form,
            'book_instance': book_instance,
        }

        return render(request, 'catalog/book_return_librarian.html', context)