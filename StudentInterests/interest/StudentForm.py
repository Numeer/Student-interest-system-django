from django import forms
from .models import Interest, Permission, Student  

class StudentForm(forms.ModelForm):
    interest_input = forms.CharField(required=False, label='Interest', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type new interest'}))
    interest = forms.ModelChoiceField(queryset=Interest.objects.all(), required=False)
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Student
        fields = ['name', 'password', 'roll_number', 'email', 'gender', 'date_of_birth','interest','permissions','city', 'department', 'degree_title', 'subject', 'start_date', 'end_date'] 
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
    
    def clean(self):
        cleaned_data = super().clean()
        interest = cleaned_data.get('interest')
        new_interest = cleaned_data.get('interest_input')

        if new_interest:
            interest, created = Interest.objects.get_or_create(name=new_interest)
            cleaned_data['interest'] = interest

        if cleaned_data.get('interest') is None:
            raise forms.ValidationError("Interest field is required.")

        return cleaned_data