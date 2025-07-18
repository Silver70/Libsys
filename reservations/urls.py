from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.reservation_list, name='reservation_list'),
    path('reserve/<int:book_id>/', views.reserve_book, name='reserve_book'),
]


