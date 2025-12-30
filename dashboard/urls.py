from django.urls import path
from . import views

urlpatterns = [
    # --- VISTAS GENERALES / PACIENTE ---
    path('', views.dashboard_view, name='dashboard'),
    path('historial-completo/', views.historial_completo_view, name='historial_completo'),
    path('borrar-historial/', views.borrar_historial, name='borrar_historial'),
    path('nueva-cita/', views.crear_cita_view, name='nueva_cita'),
    
    # NUEVA: Para ver la lista de doctores (tarjetas)
    path('lista-doctores/', views.lista_doctores_view, name='lista_doctores'),

    # --- VISTAS DEL DOCTOR ---
    path('perfil-doctor/', views.doctor_profile_view, name='doctor_profile'),
    path('editar-perfil/', views.editar_perfil_doctor, name='editar_perfil_doctor'),
    path('historial-citas/', views.historial_citas, name='historial_citas'), # Faltaba esta
    path('agenda-dia/', views.agenda_dia_view, name='agenda_dia'),

    # --- CERTIFICADOS ---
    path('perfil-doctor/certificados/', views.ver_certificados, name='ver_certificados'),
    path('perfil-doctor/certificados/accion/', views.acciones_certificados, name='acciones_certificados'),

    # --- API / AJAX (Funcionalidad asíncrona) ---
    path('api/subir-certificado/', views.subir_certificado_ajax, name='subir_certificado_ajax'),
    path('api/borrar-certificado/', views.borrar_certificado_ajax, name='borrar_certificado_ajax'),
    path('api/gestionar-cita/', views.gestionar_cita_ajax, name='gestionar_cita_ajax'), # Faltaba esta para aceptar/rechazar citas
]