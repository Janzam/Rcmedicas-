document.addEventListener('DOMContentLoaded', () => {
    console.log("✅ Sistema de Perfil Médico Vinculado");

    const config = document.getElementById('config-data');
    if (!config) return;

    const listaCertificados = document.getElementById('lista-archivos');
    const inputArchivo = document.getElementById('input-archivo');

    // --- 1. GESTIÓN DE CITAS (ACEPTAR / RECHAZAR) ---
    document.addEventListener('click', async (e) => {
        const btn = e.target.closest('.btn-gestionar');
        if (!btn) return;

        e.preventDefault();
        const { id, accion } = btn.dataset;

        if (!confirm(`¿Deseas ${accion} esta cita?`)) return;

        const formData = new FormData();
        formData.append('cita_id', id); 
        formData.append('accion', accion); 

        try {
            const response = await fetch(config.dataset.urlCita, {
                method: 'POST',
                headers: { 'X-CSRFToken': config.dataset.csrf },
                body: formData
            });
            const data = await response.json();

            if (data.status === 'success') {
                const fila = document.getElementById(`fila-cita-${id}`);
                if (fila) {
                    // Animación de salida y eliminación
                    fila.style.transition = 'all 0.4s ease';
                    fila.style.opacity = '0';
                    fila.style.transform = 'translateX(20px)';
                    setTimeout(() => {
                        fila.remove();
                        // Si era la última fila, mostrar mensaje de "No hay citas"
                        const tbody = document.querySelector('.citas-table tbody');
                        if (tbody && tbody.querySelectorAll('tr').length === 0) {
                            tbody.innerHTML = '<tr><td colspan="4"><div class="empty">No tienes citas pendientes por ahora.</div></td></tr>';
                        }
                    }, 400);
                }
            } else {
                alert("Error: " + data.message);
            }
        } catch (error) {
            console.error("Error AJAX:", error);
            alert("Error de conexión al procesar la cita.");
        }
    });

    // --- 2. GESTIÓN DE CERTIFICADOS (SUBIDA) ---
    if (inputArchivo) {
        inputArchivo.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('archivo', file);

            // Estado visual de carga
            listaCertificados.innerHTML = '<p style="padding:10px; color:#3b82f6;">📤 Subiendo...</p>';

            try {
                const response = await fetch(config.dataset.urlSubir, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': config.dataset.csrf },
                    body: formData
                });
                const data = await response.json();

                if (data.status === 'success') {
                    listaCertificados.innerHTML = `
                        <div class="file-row" id="cert-${data.id}">
                            <img src="${config.dataset.pdfIcon}" class="pdf-icon-img" alt="PDF">
                            <span class="file-name">${data.name}</span>
                            <div class="file-actions">
                                <button type="button" class="action-btn btn-delete-ajax" data-id="${data.id}">🗑️</button>
                                <a href="${data.url}" download class="action-btn">⬇️</a>
                            </div>
                        </div>`;
                }
            } catch (error) {
                alert("Error al subir archivo");
                location.reload();
            }
        });
    }

    // --- 3. GESTIÓN DE CERTIFICADOS ---
    document.addEventListener('click', async (e) => {
        const btn = e.target.closest('.btn-delete-ajax, .btn-delete-server');
        if (!btn) return;

        const id = btn.dataset.id;
        if (!confirm("¿Eliminar este certificado?")) return;

        const formData = new FormData();
        formData.append('cert_id', id); 

        try {
            const response = await fetch(config.dataset.urlBorrar, {
                method: 'POST',
                headers: { 'X-CSRFToken': config.dataset.csrf },
                body: formData
            });
            const data = await response.json();

            if (data.status === 'success') {
                document.getElementById(`cert-${id}`)?.remove();
                if (listaCertificados.children.length === 0) {
                    listaCertificados.innerHTML = '<p style="color:#a0aec0; padding:10px;">No has subido certificados recientes.</p>';
                }
            }
        } catch (error) {
            alert("Error al eliminar.");
        }
    });
});