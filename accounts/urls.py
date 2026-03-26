from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/patient/', views.register_patient_view, name='register_patient'),
    path('register/doctor/', views.register_doctor_view, name='register_doctor'),
]