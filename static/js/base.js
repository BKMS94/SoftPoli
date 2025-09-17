// Lógica del modal de detalle
document.addEventListener('DOMContentLoaded', function () {
    const detalleModal = document.getElementById('detalleModal');
    
    // Solo si el modal existe en la página, agrega el listener
    if (detalleModal) {
        const modalBody = detalleModal.querySelector('.modal-body');
        const modalTitle = detalleModal.querySelector('.modal-title');

        // Escucha el evento 'show.bs.modal' de Bootstrap
        detalleModal.addEventListener('show.bs.modal', async function (event) {
            const button = event.relatedTarget; // El botón que activó el modal
            const tipoObjeto = button.getAttribute('data-type'); // Obtiene el tipo de objeto desde el atributo 'data-type'
            const url = button.getAttribute('data-url'); // Obtiene la URL completa del objeto desde el atributo 'data-url'
            
            // Establece el título del modal de forma dinámica y muestra un mensaje de carga
            modalTitle.textContent = `Detalles de ${tipoObjeto.charAt(0).toUpperCase() + tipoObjeto.slice(1)}`;
            modalBody.innerHTML = '<p class="text-center">Cargando datos...</p>';

            try {
                // Llama a la URL que Django ha generado para obtener el HTML.
                const response = await fetch(url);
                
                if (!response.ok) {
                    throw new Error(`Error en la solicitud: ${response.status}`);
                }
                
                // La respuesta de la llamada es el HTML que Django ha renderizado.
                const htmlContent = await response.text();
                
                // Inyecta el HTML directamente en el cuerpo del modal.
                modalBody.innerHTML = htmlContent;

            } catch (error) {
                // Maneja cualquier error y muestra un mensaje en el modal
                console.error("Error al obtener los detalles del objeto:", error);
                modalBody.innerHTML = '<p class="text-danger">No se pudieron cargar los detalles. Intente de nuevo.</p>';
            }
        });
    }

    setTimeout(function () {
        const msgDiv = document.getElementById('django-messages');
        if (msgDiv) {
          msgDiv.style.transition = "opacity 0.5s";
          msgDiv.style.opacity = 0;
          setTimeout(() => msgDiv.remove(), 500);
        }
      }, 5000);
});

