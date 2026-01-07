from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm 
from dashboard.models import Doctor

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 
        'placeholder': 'Nombre'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 
        'placeholder': 'Apellidos'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-input', 
        'placeholder': 'Correo electrónico'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input', 
        'placeholder': 'Contraseña'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"] 
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class DoctorRegisterForm(RegisterForm): 
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 
        'placeholder': 'Nombre de usuario'
    }))
    
    especialidad = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input', 
        'placeholder': 'Ej: Cardiología'
    }))
    foto = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-input'
    }))

    class Meta(RegisterForm.Meta):
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'especialidad', 'foto']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está ocupado.")
        return username

    def save(self, commit=True):
        user = super(forms.ModelForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username'] 
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
            doctor = Doctor.objects.create(
                usuario=user,
                especialidad=self.cleaned_data['especialidad']
            )
            if self.cleaned_data.get('foto'):
                doctor.foto = self.cleaned_data['foto']
                doctor.save()
                
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input', 
        'placeholder': 'Usuario o Email' 
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input', 
        'placeholder': 'Contraseña'
    }))