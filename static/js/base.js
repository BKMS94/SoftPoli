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
  const kmActual   = parseFloat(kilometrajeActualInput.val() || 0);

  let diff = kmActual - kmAnterior;
  if (!Number.isFinite(diff)) diff = 0;

  // nunca negativa, con 1 decimal
  kilometrajeDiffInput.val(Math.max(0, diff).toFixed(1));
  }

  // Evento input en campo kilometraje actual
  kilometrajeActualInput.on('input', calcularDiferencia);

  // ✅ 2. Formset dinámico para piezas (sección original de base.js)
  const addBtnMovimiento = document.getElementById('add-movimiento-btn');
  const tableMovimientos = document.getElementById('movimientos-table');
  const emptyRowMovimiento = document.getElementById('empty-form-row');
  const totalFormsMovimiento = document.querySelector('input[name$="-TOTAL_FORMS"]');

  if (addBtnMovimiento && tableMovimientos && emptyRowMovimiento && totalFormsMovimiento) {
    addBtnMovimiento.addEventListener('click', function (e) {
      e.preventDefault();
      const formIdx = parseInt(totalFormsMovimiento.value);
      let newRowHtml = emptyRowMovimiento.innerHTML.replace(/__prefix__/g, formIdx);
      let newRow = document.createElement('tr');
      newRow.innerHTML = newRowHtml;
      newRow.removeAttribute('id');
      newRow.style.display = '';
      tableMovimientos.querySelector('tbody').appendChild(newRow);
      totalFormsMovimiento.value = formIdx + 1;
      attachRemoveEvents();
      setTimeout(actualizarStockEnFilas, 100);
    });

    function attachRemoveEvents() {
      tableMovimientos.querySelectorAll('.remove-row').forEach(function(btn) {
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
});


// --- Lógica de Formsets (añadir/eliminar filas) - Ahora una función global ---
window.setupFormset = function (formsetId, addBtnId, emptyFormTemplateId, prefix, initDescCallback, searchDescUrl, createDescUrl, csrfToken, initPiezaCallback, searchPiezaUrl) {
    const formsetContainer = document.getElementById(formsetId);
    const addBtn = document.getElementById(addBtnId);
    const totalFormsInput = document.querySelector(`#${formsetId} input[name$="-TOTAL_FORMS"]`);

    // Función para actualizar los prefijos de los campos (form-0-, form-1-, etc.)
    function updateElementIndex(el, prefix, ndx) {
        const idRegex = new RegExp(`(${prefix}-(\\d){1,}-)`); // Regex más robusta para índices de 1 o más dígitos
        const nameRegex = new RegExp(`(${prefix}-(\\d){1,}-)`);
        
        if (el.id) {
            el.id = el.id.replace(idRegex, `${prefix}-${ndx}-`);
        }
        if (el.name) {
            el.name = el.name.replace(nameRegex, `${prefix}-${ndx}-`);
        }
        // Actualizar data-select2-id para Select2 si existe
        if (el.hasAttribute('data-select2-id')) {
            el.setAttribute('data-select2-id', el.getAttribute('data-select2-id').replace(idRegex, `${prefix}-${ndx}-`));
        }
    }

    // Función para añadir una nueva fila
    addBtn.addEventListener('click', function() {
        const currentForms = parseInt(totalFormsInput.value);
        const newFormIndex = currentForms;
        const emptyFormHtml = document.getElementById(emptyFormTemplateId).innerHTML.replace(/__prefix__/g, newFormIndex);
        
        const newRow = document.createElement('div');
        newRow.className = 'formset-row row g-2 mb-3 align-items-center p-3 border rounded-3 bg-light-subtle animated-fade-in'; // Aplicar clases de estilo a la nueva fila
        newRow.innerHTML = emptyFormHtml;
        formsetContainer.appendChild(newRow);

        totalFormsInput.value = currentForms + 1;

        // Re-inicializar Select2 para los campos de la nueva fila, usando los callbacks pasados
        const newDescriptionInput = newRow.querySelector('.descripcion-servicio-input');
        if (newDescriptionInput && initDescCallback) {
            initDescCallback(newDescriptionInput, searchDescUrl, createDescUrl, csrfToken);
        }
        const newPiezaSelect = newRow.querySelector('select[name$="-pieza"]');
        if (newPiezaSelect && initPiezaCallback) {
            initPiezaCallback(newPiezaSelect, searchPiezaUrl);
        }

        // Añadir evento al botón de eliminar de la nueva fila
        const removeBtn = newRow.querySelector('.remove-formset-row');
        if (removeBtn) {
            removeBtn.addEventListener('click', function() {
                newRow.remove();
                updateFormsetIndexes(formsetContainer, prefix);
                totalFormsInput.value = parseInt(totalFormsInput.value) - 1;
            });
        }
    });

    // Función para actualizar índices después de eliminar una fila
    function updateFormsetIndexes(container, prefix) {
        let index = 0;
        container.querySelectorAll('.formset-row:not([style*="display: none"])').forEach(row => { // Solo las visibles
            row.querySelectorAll('input, select, textarea').forEach(el => {
                updateElementIndex(el, prefix, index);
            });
            // Actualizar label for
            row.querySelectorAll('label').forEach(label => {
                const forAttr = label.getAttribute('for');
                if (forAttr) {
                    label.setAttribute('for', forAttr.replace(new RegExp(`(${prefix}-(\\d){1,}-)`), `${prefix}-${index}-`));
                }
            });
            index++;
        });
    }

    // Añadir eventos a los botones de eliminar existentes (para edición)
    formsetContainer.querySelectorAll('.remove-formset-row').forEach(removeBtn => {
        removeBtn.addEventListener('click', function() {
            const row = removeBtn.closest('.formset-row');
            const deleteInput = row.querySelector('input[name$="-DELETE"]');
            if (deleteInput) {
                deleteInput.checked = true; // Marcar para eliminación en el backend
                row.style.display = 'none'; // Ocultar visualmente
            } else {
                row.remove(); // Eliminar directamente si no es un formulario existente
            }
            updateFormsetIndexes(formsetContainer, prefix);
            totalFormsInput.value = parseInt(totalFormsInput.value) - 1; // Actualizar TOTAL_FORMS
        });
    });

    // Para filas que ya están marcadas para DELETE (en caso de recarga por error de validación)
    formsetContainer.querySelectorAll('input[name$="-DELETE"]:checked').forEach(deleteInput => {
        deleteInput.closest('.formset-row').style.display = 'none';
    });
};

// --- Lógica de Select2 para Descripciones de Servicio - Ahora una función global ---
window.initializeSelect2Descripcion = function (element, searchUrl, createUrl, csrfToken) {
    $(element).select2({
        tags: true, // Permite crear nuevas opciones
        minimumInputLength: 2, // Mínimo de caracteres para buscar
        placeholder: 'Escribe o selecciona una descripción...',
        ajax: {
            url: searchUrl, // URL de tu API de búsqueda, pasada como argumento
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term // Término de búsqueda
                };
            },
            processResults: function (data) {
                return {
                    results: data.results // Espera un array de objetos {id: ..., text: ...}
                };
            },
            cache: true
        },
        createTag: function(params) {
            // Lógica para crear una nueva opción si no se encuentra
            const term = params.term.trim();
            if (term === '') {
                return null;
            }
            return {
                id: term, // Usamos el texto como ID temporal
                text: term,
                newTag: true // Marcamos que es una nueva etiqueta
            };
        }
    }).on('select2:select', function (e) {
        const data = e.params.data;
        // El campo oculto que guarda el FK es 'detalle' en RequerimientoDescripcionDetalle
        const hiddenInput = $(this).closest('.formset-row').find('input[name$="detalle"]'); 
        const textInput = $(this); // El propio elemento Select2

        if (data.newTag) {
            // Si es una nueva etiqueta, la creamos vía AJAX
            $.ajax({
                url: createUrl, // URL de tu API de creación, pasada como argumento
                method: 'POST',
                data: {
                    descripcion: data.text, // El nombre del parámetro que espera tu API
                    csrfmiddlewaretoken: csrfToken // Token CSRF, pasado como argumento
                },
                success: function(response) {
                    hiddenInput.val(response.id); // Asignar el ID real de la DB
                    textInput.attr('data-descripcion-id', response.id); // Guardar el ID en el data-attribute
                },
                error: function(xhr) {
                    console.error("Error al crear descripción:", xhr.responseText);
                    // Opcional: mostrar un mensaje de error al usuario
                    hiddenInput.val(''); // Limpiar si falla
                    textInput.val('').trigger('change');
                }
            });
        } else {
            // Si es una opción existente, simplemente asignamos su ID
            hiddenInput.val(data.id);
            textInput.attr('data-descripcion-id', data.id);
        }
    }).on('select2:unselect', function (e) {
        // Limpiar el campo oculto si se deselecciona
        $(this).closest('.formset-row').find('input[name$="detalle"]').val(''); 
        $(this).attr('data-descripcion-id', '');
    });

    // Si el campo ya tiene un valor inicial (en edición), Select2 necesita ser inicializado con ese valor
    if ($(element).val() || $(element).attr('data-descripcion-id')) {
        const initialId = $(element).attr('data-descripcion-id');
        const initialText = $(element).val(); // Get the initial text value
        if (initialId && initialText) {
            const option = new Option(initialText, initialId, true, true);
            $(element).append(option).trigger('change');
        }
    }
};

// --- Lógica de Select2 para Piezas - Ahora una función global ---
window.initializeSelect2Pieza = function (element, searchUrl) {
    $(element).select2({
        minimumInputLength: 2,
        placeholder: 'Busca o selecciona una pieza...',
        ajax: {
            url: searchUrl, // URL de tu API de búsqueda, pasada como argumento
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term
                };
            },
            processResults: function (data) {
                return {
                    results: data.results
                };
            },
            cache: true
            }
    });

    // Select2 maneja bien los valores iniciales de <select> ya cargados por Django.
};
