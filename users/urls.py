from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Manager-only librarian management
    path('librarians/', views.librarian_list, name='librarian_list'),
    path('librarians/create/', views.librarian_create, name='librarian_create'),
    path('librarians/<int:librarian_id>/edit/', views.librarian_edit, name='librarian_edit'),
    path('librarians/<int:librarian_id>/delete/', views.librarian_delete, name='librarian_delete'),
]