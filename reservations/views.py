from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .models import Reservation
from library.models import Book
from borrow.models import Borrowing

# Create your views here.
@login_required
def reservation_list(request):
    # Check if user is librarian
    if request.user.role != 'librarian':
        messages.error(request, "Access denied. Only librarians can view reservations.")
        return redirect('library:home')
    
    reservations = Reservation.objects.all().order_by('-created_at') # type: ignore
    
    # Pagination
    paginator = Paginator(reservations, 10)  # 10 reservations per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'reservation_list.html', {'reservations': page_obj})

@login_required
@require_POST
@csrf_protect
def approve_reservation(request, reservation_id):
    # Check if user is librarian
    if request.user.role != 'librarian':
        return HttpResponse(b'<div class="text-red-600 text-sm">Access denied.</div>') # type: ignore
    
    try:
        reservation = get_object_or_404(Reservation, id=reservation_id)
        
        if reservation.status != 'pending':
            return HttpResponse(b'<div class="text-red-600 text-sm">Only pending reservations can be approved.</div>') # type: ignore
        
        reservation.status = 'confirmed'
        reservation.save()
        
        # Return the new button HTML for HTMX
        return HttpResponse(b'''
            <button hx-post="{request.build_absolute_uri(f'/reservations/expire/{reservation.id}/')}" 
                    hx-target="closest td" 
                    hx-confirm="Are you sure you want to mark this reservation as expired?"
                    class="expire-btn bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm">
                Mark Expired
            </button>
        ''')
    except Exception as e:
        return HttpResponse(b'<div class="text-red-600 text-sm">Error: {str(e)}</div>') # type: ignore

@login_required
@require_POST
@csrf_protect
def mark_expired(request, reservation_id):
    # Check if user is librarian
    if request.user.role != 'librarian':
        return HttpResponse(b'<div class="text-red-600 text-sm">Access denied.</div>') # type: ignore
    
    try:
        reservation = get_object_or_404(Reservation, id=reservation_id)
        
        if reservation.status != 'confirmed':
            return HttpResponse(b'<div class="text-red-600 text-sm">Only confirmed reservations can be marked as expired.</div>') # type: ignore
        
        reservation.status = 'expired'
        reservation.save()
        
        # Return the final state HTML for HTMX
        return HttpResponse(b'<span class="text-gray-500 text-sm">Expired</span>') # type: ignore
    except Exception as e:
        return HttpResponse(b'<div class="text-red-600 text-sm">Error: {str(e)}</div>') # type: ignore

# Keep the existing reserve_book function as is
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