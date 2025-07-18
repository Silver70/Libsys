from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Borrowing
from .forms import BorrowingForm
from library.models import Book


# Create your views here.
def borrow_list(request):
    borrow = Borrowing.objects.all() # type: ignore
    return render(request, 'borrow_list.html', {'borrow': borrow})


@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Check if user is a member
    if request.user.role != 'member':
        messages.error(request, "Only library members can borrow books.")
        return redirect('library:book_detail', book_id=book_id)
    
    # Check if user has already borrowed this book and not returned it
    existing_borrowing = Borrowing.objects.filter( # type: ignore
        user=request.user, 
        book=book, 
        status__in=['borrowed', 'overdue']
    ).first()
    
    if existing_borrowing:
        messages.error(request, "You have already borrowed this book.")
        return redirect('library:book_detail', book_id=book_id)
    
    # Check if book is already borrowed by someone else
    book_borrowed = Borrowing.objects.filter( # type: ignore
        book=book, 
        status__in=['borrowed', 'overdue']
    ).exists()
    
    if book_borrowed:
        messages.error(request, "This book is currently borrowed. You can reserve it instead.")
        return redirect('library:book_detail', book_id=book_id)
    
    # Create new borrowing record
    borrowing = Borrowing.objects.create( # type: ignore
        user=request.user,
        book=book,
        due_date=timezone.now().date() + timedelta(days=7),
        is_extended=False,
        status='borrowed'
    )
    
    messages.success(request, f"Successfully borrowed '{book.title}'. Due date: {borrowing.due_date}")
    return redirect('library:home')


@login_required
def borrowing_history(request):
    # Get borrowings for the current user, ordered by borrow date (newest first)
    borrowings = Borrowing.objects.filter(user=request.user).order_by('-borrow_date')  # type: ignore
    return render(request, 'borrowing_history.html', {'borrowings': borrowings})
