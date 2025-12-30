document.addEventListener('DOMContentLoaded', function() {
    
    // --- 1. LÓGICA DE NAVEGACIÓN Y ACCIONES DEL DASHBOARD ---

    // Función auxiliar para redirigir
    function irA(url) {
        window.location.href = url;
    }

    // Botón: Ver Historial Completo
    const btnHistorial = document.getElementById('btn-historial-completo');
    if (btnHistorial) {
        btnHistorial.addEventListener('click', (e) => {
            e.preventDefault(); 
            irA('/dashboard/historial-completo/'); 
        });
    }

    // Botón: Ver Lista Completa de Doctores
    const btnDoctores = document.getElementById('btn-lista-doctores');
    if (btnDoctores) {
        btnDoctores.addEventListener('click', () => {
            irA('/dashboard/lista-doctores/'); 
        });
    }

    // Botón: Ver Asistencia Completa
    const btnAsistencia = document.getElementById('btn-asistencia-completa');
    if (btnAsistencia) {
        btnAsistencia.addEventListener('click', () => {
            irA('/dashboard/asistencia/'); 
        });
    }

    // Botón: Nueva Cita
    const btnNuevaCita = document.getElementById('btn-nueva-cita');
    if (btnNuevaCita) {
        btnNuevaCita.addEventListener('click', () => {
            irA('/dashboard/nueva-cita/'); 
        });
    }

    // Botón: Borrar Historial (si existe en la página)
    const btnBorrarHistorial = document.getElementById('btn-borrar-historial');
    if (btnBorrarHistorial) {
        btnBorrarHistorial.addEventListener('click', function() {
            const confirmado = confirm("⚠️ ¿Estás seguro de que quieres borrar todo tu historial?\n\nEsta acción no se puede deshacer.");
            if (confirmado) {
                window.location.href = '/dashboard/borrar-historial/';
            }
        });
    }


    // --- 2. LÓGICA DEL CALENDARIO DINÁMICO ---
    
    const daysTag = document.querySelector("#calendar-days");
    const currentMonthText = document.querySelector("#current-month");
    const prevIcon = document.querySelector("#prev-month");
    const nextIcon = document.querySelector("#next-month");

    if (daysTag && currentMonthText) {
        // Obtener fecha actual
        let date = new Date();
        let currYear = date.getFullYear();
        let currMonth = date.getMonth();

        const months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
                        "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

        const renderCalendar = () => {
            // Primer día del mes (0 Domingo, 1 Lunes...)
            let firstDayofMonth = new Date(currYear, currMonth, 1).getDay();
            // Última fecha del mes actual
            let lastDateofMonth = new Date(currYear, currMonth + 1, 0).getDate();
            // Última fecha del mes anterior
            let lastDayofLastMonth = new Date(currYear, currMonth, 0).getDate();
            // Último día de la semana del mes actual
            let lastDayofMonth = new Date(currYear, currMonth, lastDateofMonth).getDay();
            
            // Creamos los encabezados dentro del HTML para que no se borren
            let diasHTML = `
                <div class="day-name">Do</div><div class="day-name">Lu</div><div class="day-name">Ma</div>
                <div class="day-name">Mi</div><div class="day-name">Ju</div><div class="day-name">Vi</div><div class="day-name">Sa</div>
            `;

            // Días del mes anterior (grisáceos)
            for (let i = firstDayofMonth; i > 0; i--) {
                diasHTML += `<div class="day empty">${lastDayofLastMonth - i + 1}</div>`;
            }

            // Días del mes actual
            for (let i = 1; i <= lastDateofMonth; i++) {
                // Verificar si es hoy
                let isToday = i === new Date().getDate() && currMonth === new Date().getMonth() 
                             && currYear === new Date().getFullYear() ? "active-day" : "";
                
                diasHTML += `<div class="day ${isToday}">${i}</div>`;
            }

            // Días del mes siguiente (relleno)
            for (let i = lastDayofMonth; i < 6; i++) {
                diasHTML += `<div class="day empty">${i - lastDayofMonth + 1}</div>`;
            }

            // Actualizar el DOM
            currentMonthText.innerText = `${months[currMonth]} ${currYear}`;
            daysTag.innerHTML = diasHTML;

            // Agregar evento click a los días
            const days = document.querySelectorAll(".calendar-grid .day:not(.empty)");
            days.forEach(day => {
                day.addEventListener("click", () => {
                    document.querySelector(".active-day")?.classList.remove("active-day");
                    day.classList.add("active-day");
                });
            });
        };

        renderCalendar();

        // Botones Anterior / Siguiente
        prevIcon.addEventListener("click", () => {
            currMonth = currMonth - 1;
            if(currMonth < 0) {
                date = new Date(currYear, currMonth, new Date().getDate());
                currYear = date.getFullYear();
                currMonth = 11; // Diciembre
            }
            renderCalendar();
        });

        nextIcon.addEventListener("click", () => {
            currMonth = currMonth + 1;
            if(currMonth > 11) {
                date = new Date(currYear, currMonth, new Date().getDate());
                currYear = date.getFullYear();
                currMonth = 0; // Enero
            }
            renderCalendar();
        });
    }

    // --- 3. LÓGICA DE BÚSQUEDA (Si estás en la lista de doctores) ---
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.addEventListener('keyup', function(e) {
            const termino = e.target.value.toLowerCase();
            const tarjetas = document.querySelectorAll('.doctor-card');
            let encontrados = 0;

            tarjetas.forEach(card => {
                const nombre = card.querySelector('.doc-name').innerText.toLowerCase();
                const especialidad = card.querySelector('.doc-specialty').innerText.toLowerCase();

                if (nombre.includes(termino) || especialidad.includes(termino)) {
                    card.style.display = 'flex';
                    encontrados++;
                } else {
                    card.style.display = 'none';
                }
            });

            const emptyState = document.querySelector('.empty-state');
            if (emptyState) {
                if (encontrados === 0 && tarjetas.length > 0) {
                    emptyState.style.display = 'block';
                    emptyState.querySelector('p').innerText = "No se encontraron resultados.";
                } else {
                    emptyState.style.display = 'none';
                }
            }
        });
    }
});