from django.shortcuts import render, get_object_or_404
from .models import Book
from .forms import BookForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    books = Book.objects.all() # type: ignore
    context = {
        'books': books
    }
    return render(request, 'index.html', context)

def book_detail(request, book_id):
    book = Book.objects.get(id=book_id) # type: ignore
    context = {
        'book': book
    }
    return render(request, 'book_detail.html', context)


def book_add(request):
    books = Book.objects.all() # type: ignore
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = BookForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('library:home')
    context = {'form': form, 'books': page_obj}    
    return render(request, 'librarian/book_create.html', context)



def book_update(request, book_id):
    book = get_object_or_404(Book, id=book_id) # type: ignore
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('library:book_detail', book_id=book.id)
    context = {'form': form}
    return render(request, 'book_update.html', context)

def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id) # type: ignore
    book.delete()
    return redirect('library:home')