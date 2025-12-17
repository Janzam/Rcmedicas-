from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterForm, DoctorRegisterForm, LoginForm

def register_patient_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form, 'tipo': 'Paciente'})


def register_doctor_view(request):
    if request.method == 'POST':
        
        form = DoctorRegisterForm(request.POST, request.FILES) 
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('doctor_profile') 
    else:
        form = DoctorRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form, 'tipo': 'Doctor'})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if hasattr(user, 'doctor'):
                return redirect('doctor_profile') 
            else:
                return redirect('dashboard')      
                
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})