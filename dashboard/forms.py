from django import forms
from .models import Doctor, Cita

class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['especialidad', 'horario', 'telefono', 'edad', 'cedula', 'sitio_web', 'linkedin', 'descripcion', 'foto']
        
        widgets = {
            'especialidad': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: Cardiología'}),
            'horario': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: Lun-Vie 9am-5pm'}),
            'telefono': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Teléfono de contacto'}),
            'edad': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Edad'}),
            'cedula': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Cédula Profesional'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'Perfil de LinkedIn'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'maxlength': '200', 'placeholder': 'Cuéntale a tus pacientes sobre ti...'}),
            'foto': forms.FileInput(attrs={'class': 'form-input-file'}),
        }
        
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['doctor', 'fecha', 'hora', 'motivo'] # Ajusta según tus campos reales
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'motivo': forms.Textarea(attrs={'rows': 3, 'class': 'form-input', 'placeholder': 'Describa brevemente sus síntomas...'}),
            'doctor': forms.Select(attrs={'class': 'form-input select-arrow'}),
        }