from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST 
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta  # Importante para los 30 días
from .models import Doctor, Cita, Certificado 
from .forms import DoctorUpdateForm

@login_required
def dashboard_view(request):
    todos_los_doctores = Doctor.objects.all()
    doctores_disponibles = [doc for doc in todos_los_doctores if doc.esta_disponible]
    historial = Cita.objects.all().order_by('-fecha')[:5] 

    context = {
        'doctores_disponibles': doctores_disponibles,
        'historial_rapido': historial,
        'citas_pendientes': Cita.objects.filter(estado='Pendiente').count(),
        'historial_total': Cita.objects.count(),
        'proxima_cita': None
        
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def doctor_profile_view(request):
    if not hasattr(request.user, 'doctor'):
        return redirect('dashboard')
        
    doctor = request.user.doctor 
    
    # Solo mostramos los que NO están en papelera
    lista_certificados = doctor.certificados.filter(fecha_eliminacion__isnull=True).order_by('-fecha_subida')

    citas_pendientes = Cita.objects.filter(doctor=doctor, estado='Pendiente').order_by('fecha')

    context = {
        'doctor': doctor,
        'certificados': lista_certificados,
        'citas_pendientes': citas_pendientes, 
    }
    return render(request, 'dashboard/doctor_profile.html', context)


@login_required
def editar_perfil_doctor(request):
    if not hasattr(request.user, 'doctor'):
        return redirect('dashboard')
    
    doctor = request.user.doctor
    
    if request.method == 'POST':
        form = DoctorUpdateForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_profile') 
    else:
        form = DoctorUpdateForm(instance=doctor)
        
    return render(request, 'dashboard/editar_perfil.html', {'form': form})


@login_required
def historial_citas(request):
    """Página dedicada para ver TODO el historial (aceptadas, rechazadas, pasadas)"""
    if not hasattr(request.user, 'doctor'):
        return redirect('dashboard')

    doctor = request.user.doctor
    todas_las_citas = Cita.objects.filter(doctor=doctor).order_by('-fecha')
    
    return render(request, 'dashboard/historial_citas.html', {'todas_las_citas': todas_las_citas})


# --- NUEVAS VISTAS DE CERTIFICADOS (LÓGICA PAPELERA) ---

@login_required
def ver_certificados(request):
    """Vista principal de gestión de archivos con Papelera"""
    if not hasattr(request.user, 'doctor'):
        return redirect('dashboard')
    
    doctor = request.user.doctor

    # 1. LIMPIEZA AUTOMÁTICA: Borrar físicos si llevan más de 30 días en papelera
    fecha_limite = timezone.now() - timedelta(days=30)
    certificados_vencidos = Certificado.objects.filter(
        doctor=doctor, 
        fecha_eliminacion__isnull=False, 
        fecha_eliminacion__lt=fecha_limite
    )
    for cert in certificados_vencidos:
        cert.archivo.delete() # Borra el archivo físico
        cert.delete()         # Borra el registro de la BD

    # 2. OBTENER LISTAS (Activos vs Papelera)
    activos = Certificado.objects.filter(doctor=doctor, fecha_eliminacion__isnull=True).order_by('-fecha_subida')
    papelera = Certificado.objects.filter(doctor=doctor, fecha_eliminacion__isnull=False).order_by('-fecha_eliminacion')
    
    return render(request, 'dashboard/ver_certificados.html', {
        'activos': activos,
        'papelera': papelera
    })


@login_required
def acciones_certificados(request):
    """Procesa acciones en lote: Mover a papelera, Restaurar o Vaciar"""
    if request.method == 'POST':
        if not hasattr(request.user, 'doctor'):
            return redirect('dashboard')

        accion = request.POST.get('accion')
        ids = request.POST.getlist('certificados_ids')
        
        # Filtro de seguridad: solo modificar mis propios certificados
        certificados = Certificado.objects.filter(id__in=ids, doctor=request.user.doctor)

        if accion == 'papelera':
            # Soft Delete
            certificados.update(fecha_eliminacion=timezone.now())
            
        elif accion == 'restaurar':
            # Recuperar
            certificados.update(fecha_eliminacion=None)
            
        elif accion == 'vaciar_papelera':
            # Borrar TODO lo que está en papelera del usuario actual
            items_papelera = Certificado.objects.filter(doctor=request.user.doctor, fecha_eliminacion__isnull=False)
            for item in items_papelera:
                item.archivo.delete() # Borra archivo físico
                item.delete()         # Borra registro

    return redirect('ver_certificados')


# --- API / AJAX FUNCTIONS ---

@login_required
def subir_certificado_ajax(request):
    """AJAX: Sube archivo desde el perfil principal"""
    if request.method == 'POST' and request.FILES.get('archivo'):
        try:
            if not hasattr(request.user, 'doctor'):
                 return JsonResponse({'status': 'error', 'message': 'Usuario no es doctor'})

            doctor = request.user.doctor
            archivo_recibido = request.FILES['archivo']
            
            nuevo_cert = Certificado.objects.create(
                doctor=doctor,
                archivo=archivo_recibido
            )
            
            return JsonResponse({
                'status': 'success', 
                'id': nuevo_cert.id,
                'url': nuevo_cert.archivo.url,
                'name': nuevo_cert.archivo.name.split('/')[-1]
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'No se envió archivo'})


@login_required
def borrar_certificado_ajax(request):
    """AJAX: Borra desde el perfil principal -> AHORA ENVÍA A PAPELERA"""
    if request.method == 'POST':
        try:
            if not hasattr(request.user, 'doctor'):
                 return JsonResponse({'status': 'error', 'message': 'Usuario no es doctor'})

            doctor = request.user.doctor
            cert_id = request.POST.get('cert_id')
            
            cert = get_object_or_404(Certificado, id=cert_id, doctor=doctor)
            
            # CAMBIO IMPORTANTE: Soft Delete en lugar de Hard Delete
            # Así, si borras desde el perfil, lo puedes recuperar en la vista de certificados
            cert.fecha_eliminacion = timezone.now()
            cert.save()
                
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})


@login_required
@require_POST
def gestionar_cita_ajax(request):
    """AJAX: Aceptar, Rechazar o Eliminar citas"""
    try:
        if not hasattr(request.user, 'doctor'):
             return JsonResponse({'status': 'error', 'message': 'No autorizado'})

        cita_id = request.POST.get('cita_id')
        accion = request.POST.get('accion') 
        
        cita = get_object_or_404(Cita, id=cita_id, doctor=request.user.doctor)

        if accion == 'aceptar':
            cita.estado = 'Aceptada' 
            cita.save()
        elif accion == 'rechazar':
            cita.estado = 'Rechazada'
            cita.save()
        elif accion == 'eliminar':
            cita.delete() 
        
        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
@login_required
def agenda_dia_view(request):
    """
    Vista de la agenda diaria tipo calendario.
    Por ahora puede mostrarse vacía sin problema.
    """
    if not hasattr(request.user, 'doctor'):
        return redirect('dashboard')

    doctor = request.user.doctor

    # Más adelante puedes filtrar por día
    citas = Cita.objects.filter(doctor=doctor).order_by('fecha')

    context = {
        'citas': citas
    }

    return render(request, 'dashboard/agenda_dia.html', context)
