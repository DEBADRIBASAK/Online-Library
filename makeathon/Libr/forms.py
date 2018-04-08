from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=('username','Name','RollNo','Branch','Pic')


class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','password')

