from django import forms
from .models import Branch, Section

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['branch_name', 'location']
        widgets = {
            'branch_name': forms.TextInput(attrs={
                'class': 'w-full h-12 px-4 py-3 border border-[#D1D5DB] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#FF8A65] focus:border-[#FF8A65]',
                'placeholder': 'Enter branch name'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full h-12 px-4 py-3 border border-[#D1D5DB] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#FF8A65] focus:border-[#FF8A65]',
                'placeholder': 'Enter branch location'
            })
        }

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'branch_id']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full h-12 px-4 py-3 border border-[#D1D5DB] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#FF8A65] focus:border-[#FF8A65]',
                'placeholder': 'Enter section name'
            }),
            'branch_id': forms.Select(attrs={
                'class': 'w-full h-12 px-4 py-3 border border-[#D1D5DB] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#FF8A65] focus:border-[#FF8A65]'
            })
        } 