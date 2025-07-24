// Sidebar toggle (botón hamburguesa)
document.addEventListener('DOMContentLoaded', function () {
  const sidebar = document.querySelector('.sidebar-bs5');
  const toggleBtn = document.getElementById('sidebarToggle');
  const overlay = document.getElementById('sidebar-overlay');

  function openSidebar() {
    sidebar.classList.remove('d-none');
    // Forzar reflow para transición
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
      if (sidebar.classList.contains('active')) {
        closeSidebar();
      } else {
        openSidebar();
      }
    });
    overlay.addEventListener('click', function () {
      closeSidebar();
    });
  }

  // Autocierre de alertas después de 4 segundos
  setTimeout(function () {
    document.querySelectorAll('.alert').forEach(function(alert) {
      alert.classList.add('fade');
      setTimeout(() => alert.remove(), 500);
    });
  }, 4000);

  // --- Formset dinámico para piezas ---
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
      // Quita el id y el display:none
      newRow.removeAttribute('id');
      newRow.style.display = '';
      table.querySelector('tbody').appendChild(newRow);
      totalForms.value = formIdx + 1;
      attachRemoveEvents();
    });
    // Adjunta eventos de eliminar a los botones existentes
    function attachRemoveEvents() {
      table.querySelectorAll('.remove-row').forEach(function(btn) {
        btn.onclick = function(e) {
          e.preventDefault();
          if (!confirm('¿Estás seguro de eliminar esta pieza?')) return;
          // Busca el checkbox DELETE en la misma fila
          let row = btn.closest('tr');
          let checkbox = row.querySelector('input[type=checkbox][name$="-DELETE"]');
          if (checkbox) {
            checkbox.checked = true;
          }
          row.style.display = 'none';
        };
      });
    }
    attachRemoveEvents();
  }

  // --- Lógica de cálculo de kilometraje (servicio/crear y editar) ---
  function calcularDiferencia() {
    const kmAnterior = parseFloat(document.getElementById('id_kilometraje_vehiculo')?.value || 0);
    const kmActual = parseFloat(document.getElementById('id_kilometraje_act')?.value || 0);
    const diff = kmActual - kmAnterior;
    const diffInput = document.getElementById('id_kilometraje_diff');
    if (diffInput) diffInput.value = diff >= 0 ? diff : 0;
  }
  const kmAct = document.getElementById('id_kilometraje_act');
  if (kmAct) {
    kmAct.addEventListener('input', calcularDiferencia);
  }
  const vehiculoSelect = document.getElementById('id_vehiculo');
  if (vehiculoSelect) {
    vehiculoSelect.addEventListener('change', function () {
      const vehiculoId = this.value;
      if (vehiculoId) {
        fetch(`/vehiculos/kilometraje/${vehiculoId}/`)
          .then(response => response.json())
          .then(data => {
            document.getElementById('id_kilometraje_vehiculo').value = data.kilometraje;
            calcularDiferencia();
          });
      } else {
        document.getElementById('id_kilometraje_vehiculo').value = 0;
        calcularDiferencia();
      }
    });
    if (vehiculoSelect.value) {
      vehiculoSelect.dispatchEvent(new Event('change'));
    }
  }

  // --- Stock dinámico en filas ---
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
        // Trigger para mostrar stock inicial si ya hay valor
        if (selectPieza.value) {
          selectPieza.dispatchEvent(new Event('change'));
        }
      }
    });
  }
  actualizarStockEnFilas();
  // También actualizar stock en nuevas filas
  if (addBtn) {
    addBtn.addEventListener('click', function() {
      setTimeout(actualizarStockEnFilas, 100);
    });
  }
});