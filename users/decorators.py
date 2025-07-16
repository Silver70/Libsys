from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def manager_required(view_func):
    """
    Decorator to check if user has manager role.
    Redirects to home page with error message if not authorized.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please log in to access this page.")
            return redirect('login')
        
        if request.user.role != 'manager':
            messages.error(request, "Access denied. Manager privileges required.")
            return redirect('library:home')
        
        return view_func(request, *args, **kwargs)
    return wrapper 