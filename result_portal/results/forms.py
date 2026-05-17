from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Student, Result, Subject, Department


class StudentUserForm(forms.ModelForm):
    """Form to set password when creating a student user."""
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none',
        'placeholder': 'Set a password for the student'
    }))

    class Meta:
        model = CustomUser
        fields = ['password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['register_number', 'full_name', 'department', 'semester', 'batch_year', 'phone', 'email', 'photo']
        widgets = {
            'register_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 22CSE001'}),
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'department': forms.Select(attrs={'class': 'form-input'}),
            'semester': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 8}),
            'batch_year': forms.NumberInput(attrs={'class': 'form-input', 'min': 2000}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+91 XXXXXXXXXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'student@email.com'}),
            'photo': forms.FileInput(attrs={'class': 'form-input'}),
        }


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'subject', 'semester', 'internal_marks', 'external_marks', 'exam_year']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-input'}),
            'subject': forms.Select(attrs={'class': 'form-input'}),
            'semester': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 8}),
            'internal_marks': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 25, 'step': '0.5'}),
            'external_marks': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 75, 'step': '0.5'}),
            'exam_year': forms.NumberInput(attrs={'class': 'form-input'}),
        }