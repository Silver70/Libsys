from django.urls import path
from . import views

app_name = 'borrow'

urlpatterns = [
    path('', views.borrow_list, name='borrow_list'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),  
]


