"""Forms for the jobs views"""
from django import forms
from .models import Job
from tinymce.widgets import TinyMCE

# form for create job view
class JobCreateForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'employment_type', 'experience_level', 'salary_range', 'qualifications', 'responsibilities', 'skills_required', 'deadline']
        # fields = ['title', 'description', 'company', 'location', 'employment_type', 'experience_level', 'salary_range', 'qualifications', 'responsibilities', 'skills_required', 'deadline']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Job Title'}),
            'description': TinyMCE(attrs={'cols': 30, 'rows': 15}),
            'location': forms.TextInput(attrs={'placeholder': 'Location'}),
            'employment_type': forms.Select(attrs={'placeholder': 'Employment Type'}),
            'experience_level': forms.Select(attrs={'placeholder': 'Experience Level'}),
            'salary_range': forms.TextInput(attrs={'placeholder': 'Salary Range'}),
            'qualifications': TinyMCE(attrs={'cols': 30, 'rows': 15}),
            'responsibilities': TinyMCE(attrs={'cols': 30, 'rows': 15}),
            'skills_required': TinyMCE(attrs={'cols': 30, 'rows': 15}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),

        }


        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # custom utilities classes
        
        text_area_class_utility = 'border-2 border-slate-600 rounded-md shadow-sm px-4 py-2 text-base text-slate-800 focus:outline-none focus:ring-2 focus:border-slate-800 focus:border-transparent '
            
        text_input_class_utility = 'border-2 border-slate-600 rounded-md shadow-sm px-4 py-2 text-base text-slate-800 focus:outline-none focus:ring-2 focus:border-slate-800 focus:border-transparent '
        
        select_class_utility = 'form-control'
        
        for field in self.fields.values():
            # make cases for different types of fields
            if field.widget.__class__.__name__ == 'Select':
                field.widget = forms.Select(attrs={'class': select_class_utility})
                
            elif field.widget.__class__.__name__ == 'DateInput':
                field.widget = forms.DateInput({'class': text_input_class_utility, 'type': 'date'})
            elif field.widget.__class__.__name__ == 'Textarea':
                field.widget.attrs.update({'class': text_area_class_utility})
            elif field.widget.__class__.__name__ == 'TextInput':
                field.widget.attrs.update({'class': text_input_class_utility})
            else:
                field.widget.attrs.update({'class': text_input_class_utility})
    



# form for update job view
