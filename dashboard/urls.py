from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('perfil-doctor/', views.doctor_profile_view, name='doctor_profile'),
    path('editar-perfil/', views.editar_perfil_doctor, name='editar_perfil_doctor'),

    path('perfil-doctor/certificados/', views.ver_certificados, name='ver_certificados'),
    path('perfil-doctor/certificados/accion/', views.acciones_certificados, name='acciones_certificados'),

    path('api/subir-certificado/', views.subir_certificado_ajax, name='subir_certificado_ajax'),
    path('api/borrar-certificado/', views.borrar_certificado_ajax, name='borrar_certificado_ajax'),
    
     path('agenda-dia/', views.agenda_dia_view, name='agenda_dia'),
]