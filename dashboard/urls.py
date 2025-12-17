from django.urls import path
from . import views

urlpatterns = [
    # --- Vistas Principales ---
    path('', views.dashboard_view, name='dashboard'),
    path('perfil-doctor/', views.doctor_profile_view, name='doctor_profile'),
    path('editar-perfil/', views.editar_perfil_doctor, name='editar_perfil_doctor'),
    path('perfil-doctor/historial-citas/', views.historial_citas, name='historial_citas'),

    # --- NUEVAS Vistas de Gestión de Certificados (Con Papelera) ---
    path('perfil-doctor/certificados/', views.ver_certificados, name='ver_certificados'),
    path('perfil-doctor/certificados/accion/', views.acciones_certificados, name='acciones_certificados'),

    # --- API / AJAX (Para funcionalidad dinámica en el perfil) ---
    path('api/subir-certificado/', views.subir_certificado_ajax, name='subir_certificado_ajax'),
    path('api/borrar-certificado/', views.borrar_certificado_ajax, name='borrar_certificado_ajax'),
    path('api/gestionar-cita/', views.gestionar_cita_ajax, name='gestionar_cita_ajax'), 
]