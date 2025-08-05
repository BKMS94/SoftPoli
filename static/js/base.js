// ✅ 1. Inicializar Select2 correctamente (si se usa)
$(document).ready(function () {
  const vehiculoSelect = $('#id_vehiculo');
  const kilometrajeAnteriorInput = $('#id_kilometraje_vehiculo');
  const kilometrajeActualInput = $('#id_kilometraje_act');
  const kilometrajeDiffInput = $('#id_kilometraje_diff');

  // Inicializa select2 si no lo has hecho antes
  if (vehiculoSelect.length && !vehiculoSelect.hasClass('select2-hidden-accessible')) {
    vehiculoSelect.select2();
  }

  // Evento Select2: selecciona vehículo y busca kilometraje
  vehiculoSelect.on('select2:select', function (e) {
    const vehiculoId = e.params.data.id;
    console.log("Vehículo seleccionado:", vehiculoId);

    fetch(`/vehiculos/kilometraje/${vehiculoId}/`)
      .then(response => response.json())
      .then(data => {
        kilometrajeAnteriorInput.val(data.kilometraje);
        calcularDiferencia();
        console.log(data.kilometraje);
      })
      .catch(error => {
        console.error("Error al obtener el kilometraje:", error);
        kilometrajeAnteriorInput.val(0);
        calcularDiferencia();
      });
  });

  // Función: calcular diferencia de kilometraje
  function calcularDiferencia() {
    const kmAnterior = parseFloat(kilometrajeAnteriorInput.val() || 0);
    const kmActual = parseFloat(kilometrajeActualInput.val() || 0);
    const diff = kmActual - kmAnterior;
    kilometrajeDiffInput.val(diff >= 0 ? diff : 0);
  }

  // Evento input en campo kilometraje actual
  kilometrajeActualInput.on('input', calcularDiferencia);

  // ✅ 2. Formset dinámico para piezas
  const addBtn = document.getElementById('add-movimiento-btn');
  const table = document.getElementById('movimientos-table');
  const emptyRow = document.getElementById('empty-form-row');
  const totalForms = document.querySelector('input[name$="-TOTAL_FORMS"]');

  if (addBtn && table && emptyRow && totalForms) {
    addBtn.addEventListener('click', function (e) {
      e.preventDefault();
      const formIdx = parseInt(totalForms.value);
      let newRowHtml = emptyRow.innerHTML.replace(/__prefix__/g, formIdx);
      let newRow = document.createElement('tr');
      newRow.innerHTML = newRowHtml;
      newRow.removeAttribute('id');
      newRow.style.display = '';
      table.querySelector('tbody').appendChild(newRow);
      totalForms.value = formIdx + 1;
      attachRemoveEvents();
      setTimeout(actualizarStockEnFilas, 100);
    });

    function attachRemoveEvents() {
      table.querySelectorAll('.remove-row').forEach(function(btn) {
        btn.onclick = function(e) {
          e.preventDefault();
          if (!confirm('¿Estás seguro de eliminar esta pieza?')) return;
          let row = btn.closest('tr');
          let checkbox = row.querySelector('input[type=checkbox][name$="-DELETE"]');
          if (checkbox) checkbox.checked = true;
          row.style.display = 'none';
        };
      });
    }

    function actualizarStockEnFilas() {
      document.querySelectorAll('#movimientos-table tbody tr').forEach(function(row) {
        const selectPieza = row.querySelector('select');
        const stockSpan = row.querySelector('.stock-info');
        if (selectPieza && stockSpan) {
          selectPieza.onchange = function() {
            const piezaId = this.value;
            if (piezaId) {
              fetch(`/piezas/stock/${piezaId}/`)
                .then(response => response.json())
                .then(data => {
                  stockSpan.textContent = '(Stock: ' + data.stock + ')';
                });
            } else {
              stockSpan.textContent = '(Stock: -)';
            }
          };
          if (selectPieza.value) {
            selectPieza.dispatchEvent(new Event('change'));
          }
        }
      });
    }

    attachRemoveEvents();
    actualizarStockEnFilas();
  }

  // ✅ 3. Auto-cierre de alertas
  setTimeout(function () {
    document.querySelectorAll('.alert').forEach(function(alert) {
      alert.classList.add('fade');
      setTimeout(() => alert.remove(), 500);
    });
  }, 4000);

  // ✅ 4. Sidebar toggle
  const sidebar = document.querySelector('.sidebar-bs5');
  const toggleBtn = document.getElementById('sidebarToggle');
  const overlay = document.getElementById('sidebar-overlay');

  function openSidebar() {
    sidebar.classList.remove('d-none');
    void sidebar.offsetWidth;
    sidebar.classList.add('active');
    overlay.classList.add('active');
  }

  function closeSidebar() {
    sidebar.classList.remove('active');
    overlay.classList.remove('active');
    setTimeout(() => sidebar.classList.add('d-none'), 300);
  }

  if (sidebar && toggleBtn && overlay) {
    toggleBtn.addEventListener('click', function () {
      sidebar.classList.contains('active') ? closeSidebar() : openSidebar();
    });
    overlay.addEventListener('click', closeSidebar);
  }

});

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
});