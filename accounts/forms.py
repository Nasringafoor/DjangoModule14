from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student
from django import forms

class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2' ]
        
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age']

StudentFormSet = forms.modelformset_factory(
    Student,
    form=StudentForm,
    extra=2
)