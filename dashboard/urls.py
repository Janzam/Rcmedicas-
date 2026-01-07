from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('historial-completo/', views.historial_completo_view, name='historial_completo'),
    path('borrar-historial/', views.borrar_historial, name='borrar_historial'),
    path('asistencia/', views.ver_asistencia, name='ver_asistencia'),
    path('doctores/<str:especialidad>/', views.lista_doctores_view, name='lista_doctores_filtro'),
    path('especialidades/', views.especialidades_view, name='especialidades'),
    
    path('agendar/directo/<int:doctor_id>/', views.agendar_cita_doctor, name='agendar_cita_doctor'),
    path('citas-pendientes/', views.ver_citas_pendientes, name='ver_citas_pendientes'),
    
    path('perfil-doctor/', views.doctor_profile_view, name='doctor_profile'),
    path('perfil-doctor/editar/', views.editar_perfil_doctor, name='editar_perfil_doctor'),
    
    path('agenda-dia/', views.agenda_dia_view, name='agenda_dia'),
    path('cita/atender/<int:cita_id>/', views.marcar_atendida, name='marcar_atendida'),
    
    path('perfil-doctor/certificados/', views.ver_certificados, name='ver_certificados'),
    path('perfil-doctor/certificados/accion/', views.acciones_certificados, name='acciones_certificados'),

    path('api/subir-certificado/', views.subir_certificado_ajax, name='subir_certificado_ajax'),
    path('api/borrar-certificado/', views.borrar_certificado_ajax, name='borrar_certificado_ajax'),
    path('api/gestionar-cita/', views.gestionar_cita_ajax, name='gestionar_cita_ajax'),
]