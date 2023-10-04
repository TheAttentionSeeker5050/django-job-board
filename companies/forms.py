from django import forms
from .models import Company

# use custom form for company creation
class CompanyCreateForm(forms.ModelForm):
    """Form for creating a new company"""
    class Meta:
        model = Company
        fields = ['company_name', 'industry', 'location']

    
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # make string field for text input class
        form_input_utility_classes = 'border-2 border-slate-800 rounded-md shadow-sm px-4 py-2 text-base text-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-600 focus:border-transparent '

        for field in self.fields.values():
            field.widget.attrs.update({'class': form_input_utility_classes})