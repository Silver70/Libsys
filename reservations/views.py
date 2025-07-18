from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reservation
from library.models import Book
from borrow.models import Borrowing

# Create your views here.
def reservation_list(request):
    reservations = Reservation.objects.all() # type: ignore
    return render(request, 'reservation_list.html', {'reservations': reservations})


@login_required
def reserve_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Main check: Does user already have a reservation for this book?
    existing_reservation = Reservation.objects.filter( # type: ignore
        user=request.user, 
        book=book,
        status__in=['pending', 'confirmed']
    ).first()
    
    if existing_reservation:
        messages.error(request, "You have already requested a reservation for this book.")
        return redirect('library:book_detail', book_id=book_id)
    
    # Create new reservation
    reservation = Reservation.objects.create( # type: ignore
        user=request.user,
        book=book,
        status='pending',
        type='regular'
    )
    
    messages.success(request, f"Successfully reserved '{book.title}'. Your reservation is pending approval.")
    return redirect('library:book_detail', book_id=book_id)




   