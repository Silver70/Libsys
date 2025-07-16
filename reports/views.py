from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from users.decorators import manager_required
from borrow.models import Borrowing
from fines.models import Fine
from library.models import Book

@login_required
@manager_required
def reports_dashboard(request):
    """Reports dashboard - Manager only"""
    return render(request, 'reports/dashboard.html')

@login_required
@manager_required
def book_lending_report(request):
    """Book lending report - Manager only"""
    # Get date range from request or default to last 30 days
    days = request.GET.get('days', 30)
    try:
        days = int(days)
    except ValueError:
        days = 30
    
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Get borrowing statistics
    borrowings = Borrowing.objects.filter(
        borrow_date__gte=start_date,
        borrow_date__lte=end_date
    )
    
    # Total borrowings
    total_borrowings = borrowings.count()
    
    # Borrowings by status
    status_counts = borrowings.values('status').annotate(count=Count('id'))
    
    # Most borrowed books
    popular_books = borrowings.values('book__title').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Borrowings by day
    daily_borrowings = borrowings.extra(
        select={'day': 'date(borrow_date)'}
    ).values('day').annotate(count=Count('id')).order_by('day')
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'days': days,
        'total_borrowings': total_borrowings,
        'status_counts': status_counts,
        'popular_books': popular_books,
        'daily_borrowings': daily_borrowings,
    }
    
    return render(request, 'reports/book_lending_report.html', context)

@login_required
@manager_required
def overdue_books_report(request):
    """Overdue books report - Manager only"""
    today = timezone.now().date()
    
    # Get overdue borrowings
    overdue_borrowings = Borrowing.objects.filter(
        due_date__lt=today,
        status__in=['borrowed', 'overdue']
    ).select_related('user', 'book')
    
    # Overdue statistics
    total_overdue = overdue_borrowings.count()
    # Note: Book model doesn't have price field, so we'll use 0 for now
    total_overdue_amount = 0
    
    # Overdue by days
    overdue_by_days = []
    for borrowing in overdue_borrowings:
        days_overdue = (today - borrowing.due_date).days
        overdue_by_days.append({
            'borrowing': borrowing,
            'days_overdue': days_overdue
        })
    
    # Sort by days overdue (most overdue first)
    overdue_by_days.sort(key=lambda x: x['days_overdue'], reverse=True)
    
    context = {
        'overdue_borrowings': overdue_by_days,
        'total_overdue': total_overdue,
        'total_overdue_amount': total_overdue_amount,
        'today': today,
    }
    
    return render(request, 'reports/overdue_books_report.html', context)

@login_required
@manager_required
def revenue_report(request):
    """Revenue from fines report - Manager only"""
    # Get date range from request or default to last 30 days
    days = request.GET.get('days', 30)
    try:
        days = int(days)
    except ValueError:
        days = 30
    
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Get fines data
    fines = Fine.objects.filter(
        borrowing__borrow_date__gte=start_date,
        borrowing__borrow_date__lte=end_date
    )
    
    # Total revenue
    total_revenue = fines.filter(paid=True).aggregate(
        total=Sum('amount', default=0)
    )['total'] or 0
    
    # Unpaid fines
    unpaid_fines = fines.filter(paid=False)
    unpaid_amount = unpaid_fines.aggregate(
        total=Sum('amount', default=0)
    )['total'] or 0
    
    # Fines by day
    daily_fines = fines.filter(paid=True).extra(
        select={'day': 'date(paid_at)'}
    ).values('day').annotate(
        total=Sum('amount')
    ).order_by('day')
    
    # Fines by amount range
    fine_ranges = [
        {'min': 0, 'max': 10, 'label': '$0 - $10'},
        {'min': 10, 'max': 25, 'label': '$10 - $25'},
        {'min': 25, 'max': 50, 'label': '$25 - $50'},
        {'min': 50, 'max': 100, 'label': '$50 - $100'},
        {'min': 100, 'max': None, 'label': '$100+'},
    ]
    
    fines_by_range = []
    for range_info in fine_ranges:
        if range_info['max']:
            count = fines.filter(
                amount__gte=range_info['min'],
                amount__lt=range_info['max']
            ).count()
        else:
            count = fines.filter(amount__gte=range_info['min']).count()
        
        fines_by_range.append({
            'range': range_info['label'],
            'count': count
        })
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'days': days,
        'total_revenue': total_revenue,
        'unpaid_amount': unpaid_amount,
        'daily_fines': daily_fines,
        'fines_by_range': fines_by_range,
        'total_fines': fines.count(),
        'paid_fines': fines.filter(paid=True).count(),
        'unpaid_fines': unpaid_fines.count(),
    }
    
    return render(request, 'reports/revenue_report.html', context) 