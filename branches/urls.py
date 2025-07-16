from django.urls import path
from . import views

app_name = 'branches'

urlpatterns = [
    # Branch management
    path('', views.branch_list, name='branch_list'),
    path('create/', views.branch_create, name='branch_create'),
    path('<int:branch_id>/edit/', views.branch_edit, name='branch_edit'),
    path('<int:branch_id>/delete/', views.branch_delete, name='branch_delete'),
    
    # Section management
    path('sections/', views.section_list, name='section_list'),
    path('sections/create/', views.section_create, name='section_create'),
] 