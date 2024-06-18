from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Patient_Record, Profile, Patient

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    doctor = forms.ChoiceField(choices=[
        ('', 'Должность'),
        ('is_radiologist', 'Рентгенолог'),
        ('is_gynecologist', 'Гинеколог'),
        ('is_ophthalmologist', 'Офтальмолог'),
        ('is_cardiologist', 'Кардиолог'),
        ('is_procedural_nurse', 'Процедурная медицинская сестра (анализы)'),
        ('is_mammologist', 'Маммолог'),
        ('is_urologist', 'Уролог'),
        ('is_therapist', 'Терапевт'),
    ],widget=forms.Select(attrs={'class': 'error-message'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'error-message'}))
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={'class': 'error-message'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['email','username','password1', 'password2']:
            self.fields[fieldname].help_text = None
            
    def save(self, commit=True):
        user = super().save(commit=False)
        
        if commit:
            user.save()
            Profile.objects.create(user=user, doctor=self.cleaned_data['doctor'], doctorLogin=user.username, doctorMail = self.cleaned_data['email'])
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'doctor']


