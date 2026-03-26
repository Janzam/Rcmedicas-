document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('input-archivo');
    const lista = document.getElementById('lista-archivos');
    const toggleContainer = document.getElementById('toggle-container');
    const btnVerTodos = document.getElementById('btn-ver-todos');
    const config = document.getElementById('config-data');

    if (!config) return;

    if(btnVerTodos) {
        btnVerTodos.addEventListener('click', function(e) {
            e.preventDefault();
            if (lista.classList.contains('expanded')) {
                lista.classList.remove('expanded');
                this.innerText = `Ver todos mis certificados (${lista.children.length})`;
            } else {
                lista.classList.add('expanded');
                this.innerText = "Ver menos";
            }
        });
    }

    if(input){
        input.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if(!file) return;
            const tempMsg = document.createElement('div');
            tempMsg.innerText = "Subiendo...";
            tempMsg.style.color = "#007bff";
            tempMsg.style.padding = "15px 0";
            lista.prepend(tempMsg);
            const formData = new FormData();
            formData.append('archivo', file);
            try {
                const response = await fetch(config.dataset.urlSubir, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': config.dataset.csrf },
                    body: formData
                });
                const data = await response.json();
                tempMsg.remove();
                if(data.status === 'success') {
                    agregarFilaAlPrincipio(data.name, data.url, data.id);
                } else { alert('Error: ' + data.message); }
            } catch (error) { tempMsg.remove(); console.error(error); }
            input.value = '';
        });
    }

    function agregarFilaAlPrincipio(nombre, urlDescarga, certId) {
        const row = document.createElement('div');
        row.className = 'file-row';
        row.id = `cert-${certId}`;
        row.innerHTML = `
            <img src="${config.dataset.pdfIcon}" class="pdf-icon-img" alt="PDF">
            <span class="file-name">${nombre}</span> 
            <div class="file-actions">
                <button type="button" class="action-btn btn-delete-ajax" data-id="${certId}">🗑️</button>
                <a href="${urlDescarga}" download class="action-btn">⬇️</a>
            </div>
        `;
        const delBtn = row.querySelector('.btn-delete-ajax');
        if(delBtn) delBtn.addEventListener('click', () => borrarArchivo(certId, row));
        lista.prepend(row); 
        const total = lista.children.length;
        if(btnVerTodos) btnVerTodos.innerText = `Ver todos mis certificados (${total})`;
        if(total > 3) toggleContainer.style.display = 'block';
    }

    async function borrarArchivo(id, elementoDOM) {
        if(!confirm('¿Eliminar certificado?')) return;
        const formData = new FormData();
        formData.append('cert_id', id);
        try {
            const response = await fetch(config.dataset.urlBorrar, {
                method: 'POST',
                headers: { 'X-CSRFToken': config.dataset.csrf },
                body: formData
            });
            const data = await response.json();
            if(data.status === 'success') {
                elementoDOM.remove();
                const total = lista.children.length;
                if(btnVerTodos) btnVerTodos.innerText = `Ver todos mis certificados (${total})`;
                if(total <= 3) {
                    if(toggleContainer) toggleContainer.style.display = 'none';
                    lista.classList.remove('expanded');
                }
            } else { alert('Error al borrar'); }
        } catch (error) { console.error(error); }
    }

    const manageBtnHandler = (btn) => {
        btn.addEventListener('click', async function(e) {
            e.preventDefault();
            e.stopPropagation();
            const citaId = this.dataset.id;
            const accion = this.dataset.action;
            const btnActual = this;
            
            if (accion === 'cancelar' || accion === 'rechazar') {
                if (!confirm('¿Seguro que deseas cancelar/rechazar esta cita?')) return;
            }

            const formData = new FormData();
            formData.append('cita_id', citaId);
            formData.append('accion', accion);
            
            try {
                const response = await fetch(config.dataset.urlCita, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': config.dataset.csrf },
                    body: formData
                });
                const data = await response.json();
                if(data.status === 'success') {
                    // Recargar suavemente para ver cambios de estado
                    window.location.reload();
                } else { alert('Error: ' + data.message); }
            } catch (error) { console.error(error); }
        });
    };

    document.querySelectorAll('.btn-accept-appointment, .btn-manage-appointment').forEach(btn => {
        if (!btn.dataset.action) btn.dataset.action = 'aceptar';
        manageBtnHandler(btn);
    });

    // --- DROPDOWN LOGIC ---
    const marcarLeidas = async () => {
        try {
            await fetch(config.dataset.urlMarcarNotifs, {
                method: 'POST',
                headers: { 'X-CSRFToken': config.dataset.csrf }
            });
            const dot = document.querySelector('.notif-dot');
            if(dot) dot.style.display = 'none';
        } catch (e) { console.error(e); }
    };

    document.addEventListener('click', (e) => {
        // Cerrar todos los dropdowns
        document.querySelectorAll('.dropdown-menu, .nav-dropdown, .notif-dropdown').forEach(d => {
            if(!d.parentElement.contains(e.target)) {
                d.classList.remove('show');
            }
        });

        // Toggle para cualquier trigger de dropdown
        const trigger = e.target.closest('.nav-profile, .notif-bell, .actions-dropdown');
        if(trigger) {
            e.stopPropagation();
            const d = trigger.querySelector('.nav-dropdown, .notif-dropdown, .dropdown-menu');
            if(d) {
                d.classList.toggle('show');
                if(d.classList.contains('show') && trigger.classList.contains('notif-bell')) {
                    marcarLeidas();
                }
            }
        }
    });
});