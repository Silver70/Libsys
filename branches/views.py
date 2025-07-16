from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import manager_required
from .models import Branch, Section
from .forms import BranchForm, SectionForm

@login_required
@manager_required
def branch_list(request):
    """List all branches - Manager only"""
    branches = Branch.objects.all()
    return render(request, 'branches/branch_list.html', {'branches': branches})

@login_required
@manager_required
def branch_create(request):
    """Create new branch - Manager only"""
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Branch created successfully!")
            return redirect('branches:branch_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BranchForm()
    
    return render(request, 'branches/branch_form.html', {'form': form, 'title': 'Add New Branch'})

@login_required
@manager_required
def branch_edit(request, branch_id):
    """Edit existing branch - Manager only"""
    branch = get_object_or_404(Branch, id=branch_id)
    
    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            messages.success(request, "Branch updated successfully!")
            return redirect('branches:branch_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BranchForm(instance=branch)
    
    return render(request, 'branches/branch_form.html', {
        'form': form, 
        'title': f'Edit Branch: {branch.branch_name}'
    })

@login_required
@manager_required
def branch_delete(request, branch_id):
    """Delete branch - Manager only"""
    branch = get_object_or_404(Branch, id=branch_id)
    
    if request.method == 'POST':
        branch.delete()
        messages.success(request, "Branch deleted successfully!")
        return redirect('branches:branch_list')
    
    return render(request, 'branches/branch_confirm_delete.html', {'branch': branch})

@login_required
@manager_required
def section_list(request):
    """List all sections - Manager only"""
    sections = Section.objects.select_related('branch_id').all()
    return render(request, 'branches/section_list.html', {'sections': sections})

@login_required
@manager_required
def section_create(request):
    """Create new section - Manager only"""
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Section created successfully!")
            return redirect('branches:section_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SectionForm()
    
    return render(request, 'branches/section_form.html', {'form': form, 'title': 'Add New Section'})
