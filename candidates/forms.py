from django import forms
from .models import Candidate, CustomCandidateForm

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['full_name', 'email', 'phone', 'dob', 'gender', 'address', 'position',
                 'institution', 'year_passing', 'specialization', 'skills', 'resume', 'certifications']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'position': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply form-control class to all fields not explicitly defined in Meta.widgets
        for field_name, field in self.fields.items():
            if field_name not in self.Meta.widgets:
                if not isinstance(field.widget, forms.FileInput):  # Avoid adding class to FileInput
                    field.widget.attrs.update({'class': 'form-control'})
                elif field_name == 'resume' or field_name == 'certifications':
                    field.widget.attrs.update({'class': 'form-control-file'})  # Bootstrap file input class

class CustomPrefilledCandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['full_name', 'email', 'phone', 'dob', 'gender', 'address', 'position',
                 'institution', 'year_passing', 'specialization', 'skills', 'resume', 'certifications']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'position': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, custom_form=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply form-control class to all fields not explicitly defined in Meta.widgets
        for field_name, field in self.fields.items():
            if field_name not in self.Meta.widgets:
                if not isinstance(field.widget, forms.FileInput):  # Avoid adding class to FileInput
                    field.widget.attrs.update({'class': 'form-control'})
                elif field_name == 'resume' or field_name == 'certifications':
                    field.widget.attrs.update({'class': 'form-control-file'})  # Bootstrap file input class

        # Set initial values from CustomCandidateForm if provided
        if custom_form:
            initial_data = {
                'full_name': custom_form.full_name,
                'email': custom_form.email,
                'phone': custom_form.phone,
                'dob': custom_form.dob,
                'gender': custom_form.gender,
                'address': custom_form.address,
                'position': custom_form.position,
                'institution': custom_form.institution,
                'year_passing': custom_form.year_passing,
                'specialization': custom_form.specialization,
                'skills': custom_form.skills,
            }
            self.initial.update(initial_data)
            # Make fields read-only if they have initial values
            for field_name, value in initial_data.items():
                if value:  # Only make non-null fields read-only
                    self.fields[field_name].widget.attrs['readonly'] = True