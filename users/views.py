from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import manager_required
from .forms import UserRegistrationForm, UserLoginForm
from .models import User

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('library:home')
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('library:home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('library:home')

# Manager-only views for librarian management
@login_required
@manager_required
def librarian_list(request):
    """List all librarians - Manager only"""
    librarians = User.objects.filter(role='librarian')
    return render(request, 'users/librarian_list.html', {'librarians': librarians})

@login_required
@manager_required
def librarian_create(request):
    """Create new librarian account - Manager only"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'librarian'  # Set role to librarian
            user.save()
            messages.success(request, "Librarian account created successfully!")
            return redirect('users:librarian_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/librarian_form.html', {'form': form, 'title': 'Add New Librarian'})

@login_required
@manager_required
def librarian_edit(request, librarian_id):
    """Edit librarian account - Manager only"""
    librarian = get_object_or_404(User, id=librarian_id, role='librarian')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=librarian)
        if form.is_valid():
            form.save()
            messages.success(request, "Librarian account updated successfully!")
            return redirect('users:librarian_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm(instance=librarian)
    
    return render(request, 'users/librarian_form.html', {
        'form': form, 
        'title': f'Edit Librarian: {librarian.get_full_name() or librarian.username}'
    })

@login_required
@manager_required
def librarian_delete(request, librarian_id):
    """Delete librarian account - Manager only"""
    librarian = get_object_or_404(User, id=librarian_id, role='librarian')
    
    if request.method == 'POST':
        librarian.delete()
        messages.success(request, "Librarian account deleted successfully!")
        return redirect('users:librarian_list')
    
    return render(request, 'users/librarian_confirm_delete.html', {'librarian': librarian})
