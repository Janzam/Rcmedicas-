from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Doctor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='doctores/', default='doctores/default.jpg')
    horario = models.CharField(max_length=100, default="Lun - Vie: 9am - 5pm")
    capacidad_diaria = models.IntegerField(default=10)
    
    descripcion = models.TextField(blank=True, verbose_name="Sobre mí")
    edad = models.IntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    cedula = models.CharField(max_length=20, blank=True, verbose_name="Cédula/ID")
    sitio_web = models.URLField(blank=True)
    linkedin = models.URLField(blank=True, verbose_name="Perfil de LinkedIn")

    def __str__(self):
        return f"Dr. {self.usuario.first_name} {self.usuario.last_name}"

    @property
    def esta_disponible(self):
        citas_hoy = Cita.objects.filter(doctor=self, fecha__date=timezone.now().date()).count()
        return citas_hoy < self.capacidad_diaria

class Certificado(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='certificados', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='certificados/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return f"Doc: {self.doctor.usuario.last_name} - Archivo: {self.archivo.name}"
    
    def esta_en_papelera(self):
        return self.fecha_eliminacion is not None

class Cita(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    paciente = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    motivo = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, default='Pendiente')

    def __str__(self):
        return f"Cita {self.paciente} con {self.doctor}"
