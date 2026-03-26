document.addEventListener('DOMContentLoaded', function() {
    
    function irA(url) {
        window.location.href = url;
    }

    const config = document.getElementById('config-data');

    const btnHistorial = document.getElementById('btn-historial-completo');
    if (btnHistorial) {
        btnHistorial.addEventListener('click', (e) => {
            e.preventDefault(); 
            irA('/dashboard/historial-completo/'); 
        });
    }

    const btnDoctores = document.getElementById('btn-lista-doctores');
    if (btnDoctores) {
        btnDoctores.addEventListener('click', () => {
            irA('/dashboard/lista-doctores/'); 
        });
    }

    const btnAsistencia = document.getElementById('btn-asistencia-completa');
    if (btnAsistencia) {
        btnAsistencia.addEventListener('click', () => {
            irA('/dashboard/asistencia/'); 
        });
    }

    const btnNuevaCita = document.getElementById('btn-nueva-cita');
    if (btnNuevaCita) {
        btnNuevaCita.addEventListener('click', () => {
            irA('/dashboard/nueva-cita/'); 
        });
    }

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
        let date = new Date();
        let currYear = date.getFullYear();
        let currMonth = date.getMonth();

        const months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
                        "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

        const renderCalendar = () => {
            let firstDayofMonth = new Date(currYear, currMonth, 1).getDay();
            let lastDateofMonth = new Date(currYear, currMonth + 1, 0).getDate();
            let lastDayofLastMonth = new Date(currYear, currMonth, 0).getDate();
            let lDate = new Date(currYear, currMonth, lastDateofMonth).getDay();
            
            let diasHTML = `
                <div class="day-name">Do</div><div class="day-name">Lu</div><div class="day-name">Ma</div>
                <div class="day-name">Mi</div><div class="day-name">Ju</div><div class="day-name">Vi</div><div class="day-name">Sa</div>
            `;

            for (let i = firstDayofMonth; i > 0; i--) {
                diasHTML += `<div class="day empty">${lastDayofLastMonth - i + 1}</div>`;
            }

            for (let i = 1; i <= lastDateofMonth; i++) {
                let isToday = i === new Date().getDate() && currMonth === new Date().getMonth() 
                             && currYear === new Date().getFullYear() ? "active-day" : "";
                diasHTML += `<div class="day ${isToday}">${i}</div>`;
            }

            for (let i = lDate; i < 6; i++) {
                diasHTML += `<div class="day empty">${i - lDate + 1}</div>`;
            }

            currentMonthText.innerText = `${months[currMonth]} ${currYear}`;
            daysTag.innerHTML = diasHTML;

            const days = document.querySelectorAll(".calendar-grid .day:not(.empty)");
            days.forEach(day => {
                day.addEventListener("click", () => {
                    document.querySelector(".active-day")?.classList.remove("active-day");
                    day.classList.add("active-day");
                });
            });
        };

        renderCalendar();

        prevIcon.addEventListener("click", () => {
            currMonth = currMonth - 1;
            if(currMonth < 0) {
                date = new Date(currYear, currMonth, new Date().getDate());
                currYear = date.getFullYear();
                currMonth = 11; 
            }
            renderCalendar();
        });

        nextIcon.addEventListener("click", () => {
            currMonth = currMonth + 1;
            if(currMonth > 11) {
                date = new Date(currYear, currMonth, new Date().getDate());
                currYear = date.getFullYear();
                currMonth = 0; 
            }
            renderCalendar();
        });
    }

    // --- 3. LÓGICA DE BÚSQUEDA ---
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

    // --- DROPDOWN LOGIC ---
    const marcarLeidas = async () => {
        if(!config) return;
        try {
            await fetch(config.dataset.urlMarcarNotifs, {
                method: 'POST',
                headers: { 'X-CSRFToken': config.dataset.csrf }
            });
            const dot = document.querySelector('.notif-dot');
            if(dot) dot.style.display = 'none';
        } catch (e) { console.error(e); }
    };

    const setupDropdown = (trigger, other) => {
        if(!trigger) return;
        trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            const d = trigger.querySelector('.nav-dropdown') || trigger.querySelector('.notif-dropdown');
            if(d) {
                d.classList.toggle('show');
                if(d.classList.contains('show') && trigger.classList.contains('notif-bell')) {
                    marcarLeidas();
                }
            }
            const od = other?.querySelector('.nav-dropdown') || other?.querySelector('.notif-dropdown');
            if(od) od.classList.remove('show');
        });
    };
    const np = document.querySelector('.nav-profile');
    const nb = document.querySelector('.notif-bell');
    setupDropdown(np, nb);
    setupDropdown(nb, np);
    document.addEventListener('click', () => {
        document.querySelectorAll('.nav-dropdown, .notif-dropdown').forEach(d => d.classList.remove('show'));
    });
});