from django.shortcuts import render
from .models import Reservation
from django.http import HttpResponse

# Create your views here.
def reservation_list(request):
    reservations = Reservation.objects.all() # type: ignore
    return render(request, 'reservation_list.html', {'reservations': reservations})
