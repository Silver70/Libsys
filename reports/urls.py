from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_dashboard, name='dashboard'),
    path('book-lending/', views.book_lending_report, name='book_lending'),
    path('overdue-books/', views.overdue_books_report, name='overdue_books'),
    path('revenue/', views.revenue_report, name='revenue'),
] 