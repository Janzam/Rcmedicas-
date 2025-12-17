from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm 
from dashboard.models import Doctor
class RegisterForm(forms.ModelForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input', 
        'placeholder': 'Username'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input', 
        'placeholder': 'Last name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-input', 
        'placeholder': 'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input', 
        'placeholder': 'Password'
    }))

    class Meta:
        model = User
        fields = ['username', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input', 
        'placeholder': 'username' 
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input', 
        'placeholder': 'password'
    }))


class DoctorRegisterForm(RegisterForm): 
    especialidad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: Cardiología'}))
    foto = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-input'}))

    class Meta(RegisterForm.Meta):
        fields = RegisterForm.Meta.fields + ['especialidad', 'foto']

    def save(self, commit=True):
        user = super().save(commit=True)
        doctor = Doctor.objects.create(
            usuario=user,
            especialidad=self.cleaned_data['especialidad']
        )
        if self.cleaned_data.get('foto'):
            doctor.foto = self.cleaned_data['foto']
            doctor.save()
            
        return user