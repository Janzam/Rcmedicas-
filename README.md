# RCMedicas 🏥 - Sistema de Gestión de Citas Médicas

RCMedicas es una plataforma web moderna e interactiva desarrollada con **Django** que facilita el agendamiento y la gestión de citas médicas, conectando de manera eficiente a pacientes y profesionales de la salud.

## 🚀 Requisitos Previos

Antes de instalar el proyecto, asegúrate de tener instalado:
- **Python 3.10+**
- **pip** (Administrador de paquetes de Python)
- **Git**

## 🛠️ Instalación y Configuración del Proyecto

Sigue estos pasos para poner en marcha el proyecto en tu entorno local:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Janzam/Rcmedicas-.git
   cd Rcmedicas-
   ```

2. **Crear y activar un entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Realizar las migraciones de la base de datos:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crear un superusuario (para acceder al panel administrativo):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Iniciar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

7. **Acceder a la aplicación:**
   Abre tu navegador en `http://127.0.0.1:8000/`

---

## 🧭 ¿Cómo Navegar en RCMedicas?

La aplicación está dividida en dos portales principales según el rol del usuario:

### 👤 Portal del Paciente
- **Agendamiento Rápido**: Busca doctores por su especialidad y selecciona el horario que mejor te convenga.
- **Dashboard Personal**: Visualiza un resumen de tus próximas citas y el historial total.
- **Historial Completo**: Sección dedicada para revisar todas tus consultas pasadas.
- **Sistema de Notificaciones**: Recibe alertas instantáneas en la campana superior cuando tu cita sea aceptada o rechazada.

### 🩺 Portal del Doctor
- **Dashboard de Gestión**: Visualiza tus próximas 3 citas de un vistazo.
- **Agenda Completa**: Accede a la lista detallada de todos los pacientes del día.
- **Acciones Rápidas (AJAX)**: Gestiona citas (Aceptar, Rechazar, Completar o Cancelar) sin recargar la página.
- **Gestión de Perfil**: Actualiza tu información profesional y certificados en una interfaz diseñada en rejilla.
- **Papelera de Certificados**: Administra tus documentos profesionales con un sistema de borrado temporal.

---

## 💎 Características Principales

- **Interfaz de Usuario (UI) Adaptativa**: Diseño optimizado tanto para pacientes como para doctores.
- **Interacción en Tiempo Real**: Uso masivo de AJAX para una navegación fluida y sin esperas.
- **Notificaciones Segregadas**: Cada usuario solo recibe alertas relevantes a su rol activo en el sistema.
- **Gestión de Archivos**: Soporte para subida de certificados y fotos de perfil con control de eliminación.

---

## 🧱 Estructura del Código

- `/dashboard`: Contiene la lógica de perfiles médicos, gestión de citas y templates dinámicos.
- `/accounts`: Maneja el registro diferenciado y la autenticación de usuarios.
- `/media`: Almacén de archivos subidos por los usuarios (fotos y PDFs).
- `/static`: Recursos visuales base (CSS nativo, JS modular e iconos).

## 📄 Licencia
Este proyecto es una herramienta de código abierto desarrollada para mejorar la accesibilidad médica.
