from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST 
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages 
from .models import Doctor, Cita, Certificado 
from .forms import DoctorUpdateForm, CitaForm


# 1. VISTAS DE PACIENTE / USUARIO GENERAL
@login_required
def dashboard_view(request):
    
    citas_historial = Cita.objects.filter(paciente=request.user).order_by('-fecha')
    
    doctores_recientes = []
    ids_vistos = set()
    
    for cita in citas_historial:
        if cita.doctor.id not in ids_vistos and len(doctores_recientes) < 3:
            doctores_recientes.append(cita.doctor)
            ids_vistos.add(cita.doctor.id)
    
    hoy = timezone.now().date()
    
    try:
        
        historial = Cita.objects.filter(paciente=request.user).order_by('-fecha')[:5]
        citas_pendientes = Cita.objects.filter(paciente=request.user, estado='Pendiente').count()
        historial_total = Cita.objects.filter(paciente=request.user).count()
        
        proxima_cita = Cita.objects.filter(
            paciente=request.user,
            fecha__gte=hoy
        ).exclude(
            estado='Cancelado'
        ).exclude(
            estado='Rechazada'
        ).order_by('fecha', 'hora').first()
        
    except Exception as e:
        print(f"Error cargando dashboard: {e}")
        historial = []
        citas_pendientes = 0
        historial_total = 0
        proxima_cita = None

    context = {
        'doctores_recientes': doctores_recientes, 
        'historial_rapido': historial,
        'citas_pendientes': citas_pendientes,
        'historial_total': historial_total,
        'proxima_cita': proxima_cita
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def crear_cita_view(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.paciente = request.user 
            cita.estado = 'Pendiente'
            cita.save()
            messages.success(request, '¡Tu cita ha sido agendada exitosamente!')
            return redirect('dashboard') 
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CitaForm()

    return render(request, 'dashboard/nuevas_citas.html', {'form': form})

@login_required
def especialidades_view(request):
    lista_especialidades = [
        {'nombre': 'Medicina General', 'icono': 'fa-stethoscope', 'color': '#4CAF50'},
        {'nombre': 'Odontología', 'icono': 'fa-tooth', 'color': '#2196F3'},
        {'nombre': 'Pediatría', 'icono': 'fa-baby', 'color': '#FF9800'},
        {'nombre': 'Cardiología', 'icono': 'fa-heartbeat', 'color': '#E91E63'},
        {'nombre': 'Ginecología', 'icono': 'fa-venus', 'color': '#9C27B0'},
        {'nombre': 'Dermatología', 'icono': 'fa-allergies', 'color': '#00BCD4'},
        {'nombre': 'Oftalmología', 'icono': 'fa-eye', 'color': '#3F51B5'},
        {'nombre': 'Traumatología', 'icono': 'fa-bone', 'color': '#795548'},
    ]
    
    return render(request, 'dashboard/especialidades.html', {'especialidades': lista_especialidades})

@login_required
def lista_doctores_view(request, especialidad):
    """
    Muestra la lista de doctores FILTRADA por la especialidad seleccionada.
    """
    doctores = Doctor.objects.filter(especialidad__iexact=especialidad)
    
    context = {
        'doctores': doctores,
        'especialidad_actual': especialidad
    }
    return render(request, 'dashboard/lista_doctor.html', context)

@login_required
def historial_completo_view(request):
    """Vista para ver el historial completo del PACIENTE."""
    try:
        citas = Cita.objects.filter(paciente=request.user).order_by('-fecha')
    except:
        citas = []
    context = {'historial_completo': citas}
    return render(request, 'dashboard/historial_completo.html', context)

@login_required
def borrar_historial(request):
    """Elimina todo el historial de citas del paciente actual."""
    try:
        Cita.objects.filter(paciente=request.user).delete()
        messages.success(request, "Historial eliminado correctamente.")
    except Exception as e:
        messages.error(request, "Error al eliminar historial.")
    return redirect('historial_completo') 


# 2. VISTAS DE DOCTOR
@login_required
def doctor_profile_view(request):
    if not hasattr(request.user, 'doctor'):
        return redirect('dashboard')
    doctor = request.user.doctor 
    lista_certificados = doctor.certificados.filter(fecha_eliminacion__isnull=True).order_by('-fecha_subida')
    citas_pendientes = Cita.objects.filter(doctor=doctor, estado='Pendiente').order_by('fecha')
    context = {'doctor': doctor, 'certificados': lista_certificados, 'citas_pendientes': citas_pendientes}
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
    if not hasattr(request.user, 'doctor'):
        return redirect('dashboard')
    doctor = request.user.doctor
    todas_las_citas = Cita.objects.filter(doctor=doctor).order_by('-fecha')
    return render(request, 'dashboard/historial_citas.html', {'todas_las_citas': todas_las_citas})


@login_required
def agendar_cita_doctor(request, doctor_id):
    
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        form = CitaForm(request.POST)
        
        if form.is_valid():
            cita = form.save(commit=False)
            cita.paciente = request.user 
            cita.doctor = doctor
            cita.especialidad = doctor.especialidad 
            cita.estado = 'Pendiente'
            
            cita.save()
            
            messages.success(request, f'Cita agendada con el Dr. {doctor.usuario.last_name}')
            return redirect('dashboard')
            
        else:
            
            print("Errores de validación:", form.errors)
            messages.error(request, "Error al agendar. Revisa la fecha/hora.")
            
    else:
        form = CitaForm()

    context = {
        'doctor': doctor,
        'form': form
    }
    return render(request, 'dashboard/agendar_directo.html', context)
@login_required
def ver_citas_pendientes(request):
    hoy = timezone.now().date()
    citas = Cita.objects.filter(
        paciente=request.user, 
        fecha__gte=hoy, 
        estado='Pendiente'
    ).order_by('fecha', 'hora')
    
    return render(request, 'dashboard/citas_pendientes.html', {'citas': citas})
@login_required
def ver_asistencia(request):
    citas = Cita.objects.filter(paciente=request.user).order_by('-fecha')
    
    return render(request, 'dashboard/asistencia.html', {'citas': citas})
# --- GESTIÓN DE CERTIFICADOS (PAPELERA) ---

@login_required
def ver_certificados(request):
    if not hasattr(request.user, 'doctor'):
        return redirect('dashboard')
    doctor = request.user.doctor
    fecha_limite = timezone.now() - timedelta(days=30)
    certificados_vencidos = Certificado.objects.filter(doctor=doctor, fecha_eliminacion__isnull=False, fecha_eliminacion__lt=fecha_limite)
    for cert in certificados_vencidos:
        cert.archivo.delete() 
        cert.delete() 

    activos = Certificado.objects.filter(doctor=doctor, fecha_eliminacion__isnull=True).order_by('-fecha_subida')
    papelera = Certificado.objects.filter(doctor=doctor, fecha_eliminacion__isnull=False).order_by('-fecha_eliminacion')
    return render(request, 'dashboard/ver_certificados.html', {'activos': activos, 'papelera': papelera})

@login_required
def acciones_certificados(request):
    if request.method == 'POST':
        if not hasattr(request.user, 'doctor'):
            return redirect('dashboard')
        accion = request.POST.get('accion')
        ids = request.POST.getlist('certificados_ids')
        certificados = Certificado.objects.filter(id__in=ids, doctor=request.user.doctor)
        
        if accion == 'papelera':
            certificados.update(fecha_eliminacion=timezone.now())
        elif accion == 'restaurar':
            certificados.update(fecha_eliminacion=None)
        elif accion == 'vaciar_papelera':
            items_papelera = Certificado.objects.filter(doctor=request.user.doctor, fecha_eliminacion__isnull=False)
            for item in items_papelera:
                item.archivo.delete()
                item.delete()
    return redirect('ver_certificados')

# 3. API / AJAX FUNCTIONS
@login_required
def subir_certificado_ajax(request):
    if request.method == 'POST' and request.FILES.get('archivo'):
        try:
            if not hasattr(request.user, 'doctor'):
                 return JsonResponse({'status': 'error', 'message': 'Usuario no es doctor'})
            doctor = request.user.doctor
            archivo_recibido = request.FILES['archivo']
            nuevo_cert = Certificado.objects.create(doctor=doctor, archivo=archivo_recibido)
            return JsonResponse({'status': 'success', 'id': nuevo_cert.id, 'url': nuevo_cert.archivo.url, 'name': nuevo_cert.archivo.name.split('/')[-1]})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'No se envió archivo'})

@login_required
def borrar_certificado_ajax(request):
    if request.method == 'POST':
        try:
            if not hasattr(request.user, 'doctor'):
                 return JsonResponse({'status': 'error', 'message': 'Usuario no es doctor'})
            doctor = request.user.doctor
            cert_id = request.POST.get('cert_id')
            cert = get_object_or_404(Certificado, id=cert_id, doctor=doctor)
            cert.fecha_eliminacion = timezone.now()
            cert.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

@login_required
@require_POST
def gestionar_cita_ajax(request):
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