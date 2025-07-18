from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.reservation_list, name='reservation_list'),
    path('reserve/<int:book_id>/', views.reserve_book, name='reserve_book'),
    path('approve/<int:reservation_id>/', views.approve_reservation_confirm, name='approve_reservation_confirm'),
    path('approve/confirm/<int:reservation_id>/', views.approve_reservation, name='approve_reservation'),
    path('expire/<int:reservation_id>/', views.expire_reservation_confirm, name='expire_reservation_confirm'),
    path('expire/confirm/<int:reservation_id>/', views.mark_expired, name='mark_expired'),
]


