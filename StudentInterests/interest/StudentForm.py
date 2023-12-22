from django import forms
from .models import Interest, Student  

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'password', 'roll_number', 'email', 'gender', 'date_of_birth', 'interest', 'city', 'department', 'degree_title', 'subject', 'start_date', 'end_date']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control mb-2'})
        self.fields['start_date'].widget.attrs.update({'class': 'form-control mb-2'})
        self.fields['end_date'].widget.attrs.update({'class': 'form-control mb-2'})
        