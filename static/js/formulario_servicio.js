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