from django import forms
from .models import Student  

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'password', 'roll_number', 'email', 'gender', 'date_of_birth', 'interest', 'city', 'department', 'degree_title', 'subject', 'start_date', 'end_date']
