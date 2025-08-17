// Asegúrate de que jQuery y Select2 estén disponibles globalmente.
// Si tu proyecto no los carga ya, puedes añadirlos aquí o en tu plantilla base
// antes de la carga de este script.
// <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
// <link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
// <script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>


document.addEventListener('DOMContentLoaded', function () {

    // --- Lógica Universal del Modal Dinámico (modal-completo-final) ---
    // Este script se encarga de manejar la carga de contenido en el modal de forma genérica
    // utilizando el motor de plantillas de Django para renderizar el HTML.
    const detalleModal = document.getElementById('detalleModal');
    
    // Solo si el modal existe en la página, agrega el listener
    if (detalleModal) {
        const modalBody = detalleModal.querySelector('.modal-body');
        const modalTitle = detalleModal.querySelector('.modal-title');

        // Escucha el evento 'show.bs.modal' de Bootstrap
        detalleModal.addEventListener('show.bs.modal', async function (event) {
            const button = event.relatedTarget; // El botón que activó el modal
            const tipoObjeto = button.getAttribute('data-type'); // Obtiene el tipo de objeto
            const url = button.getAttribute('data-url'); // Obtiene la URL completa del objeto
            
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


    // --- Funciones Globales para Inicialización de Select2 ---

    /**
     * Inicializa Select2 para campos de descripción de servicio con capacidad de autocompletado y creación de tags.
     * Esta función está diseñada para ser llamada desde cualquier plantilla que necesite esta funcionalidad.
     * Espera un objeto 'urls' con 'buscarDescripciones', 'crearDescripciones', y 'csrfToken'.
     * @param {HTMLElement} element El elemento input HTML al que se aplicará Select2.
     * @param {object} urls Objeto con las URLs de la API y el token CSRF.
     */
    window.initializeSelect2Descripcion = function(element, urls) {
        $(element).select2({
            tags: true, // Permite crear nuevas opciones si no se encuentran
            tokenSeparators: [',', ' '], // Separadores para tags (si se usaran múltiples, pero aquí es uno)
            minimumInputLength: 2, // Mínimo de caracteres para iniciar la búsqueda
            placeholder: 'Escribe o selecciona una descripción...',
            ajax: {
                url: urls.buscarDescripciones, // URL de la API de búsqueda de descripciones
                dataType: 'json',
                delay: 250, // Pequeño retraso para evitar llamadas excesivas
                data: function (params) {
                    return {
                        q: params.term // El término de búsqueda
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
                // Lógica para crear una nueva opción si el texto no coincide con las existentes
                const term = params.term.trim();
                if (term === '') {
                    return null;
                }
                return {
                    id: term, // Usamos el texto como ID temporal para la nueva opción
                    text: term,
                    newTag: true // Marcamos que es una nueva etiqueta para procesarla luego
                };
            }
        }).on('select2:select', function (e) {
            // Evento que se dispara cuando se selecciona una opción (existente o nueva)
            const data = e.params.data;
            // Busca el campo oculto (ForeignKey) en la misma fila del formset
            // Se usa un selector flexible para compatibilidad con 'detalle' o 'descripcion_servicio'
            const hiddenInput = $(this).closest('.formset-row').find('input[name$="-detalle"], input[name$="descripcion_servicio"]');
            const textInput = $(this); // Referencia al propio elemento Select2

            if (data.newTag) {
                // Si la opción seleccionada es una nueva tag (creada por el usuario)
                $.ajax({
                    url: urls.crearDescripciones, // URL de la API para crear descripciones
                    method: 'POST',
                    data: {
                        descripcion: data.text,
                        csrfmiddlewaretoken: urls.csrfToken // Envía el token CSRF
                    },
                    success: function(response) {
                        // Si la creación es exitosa, asigna el ID real de la base de datos
                        hiddenInput.val(response.id);
                        // Actualiza el texto visible de Select2 y su data-attribute con el ID real
                        textInput.val(response.text).trigger('change');
                        textInput.attr('data-descripcion-id', response.id);
                    },
                    error: function(xhr) {
                        console.error("Error al crear descripción:", xhr.responseText);
                        // Limpia los campos si hay un error para evitar datos inconsistentes
                        hiddenInput.val('');
                        textInput.val('').trigger('change');
                    }
                });
            } else {
                // Si la opción seleccionada ya existía en el catálogo
                hiddenInput.val(data.id); // Asigna el ID existente
                textInput.attr('data-descripcion-id', data.id); // Guarda el ID en el data-attribute
            }
        }).on('select2:unselect', function (e) {
            // Evento cuando se deselecciona una opción (limpiar el campo oculto)
            $(this).closest('.formset-row').find('input[name$="-detalle"], input[name$="descripcion_servicio"]').val('');
            $(this).attr('data-descripcion-id', '');
        });

        // Lógica para pre-inicializar Select2 si el campo ya tiene un valor (en modo edición)
        if ($(element).attr('data-descripcion-id')) {
            const initialId = $(element).attr('data-descripcion-id');
            const initialText = $(element).val();
            if (initialId && initialText) {
                const option = new Option(initialText, initialId, true, true);
                $(element).append(option).trigger('change');
            }
        }
    };

    /**
     * Inicializa Select2 para campos de Pieza (solo búsqueda).
     * Esta función está diseñada para ser llamada desde cualquier plantilla que necesite esta funcionalidad.
     * Espera un objeto 'urls' con 'buscarPiezas'.
     * @param {HTMLElement} element El elemento select HTML al que se aplicará Select2.
     * @param {object} urls Objeto con la URL de la API de búsqueda de piezas.
     */
    window.initializeSelect2Pieza = function(element, urls) {
        $(element).select2({
            placeholder: 'Selecciona una pieza...',
            allowClear: true,
            minimumInputLength: 2,
            ajax: {
                url: urls.buscarPiezas, // URL de la API de búsqueda de piezas
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
    };

    // --- Lógica Global de Formsets (añadir/eliminar filas) ---

    /**
     * Configura la lógica para añadir y eliminar filas en un formset dinámico de Django.
     * @param {string} formsetId El ID del contenedor principal del formset (ej. 'requerimiento-servicios-formset').
     * @param {string} addBtnId El ID del botón para añadir nuevas filas (ej. 'add-requerimiento-servicio').
     * @param {string} emptyFormTemplateId El ID de la plantilla HTML oculta (<template>) para una nueva fila.
     * @param {string} prefix El prefijo del formset (ej. 'serviciodetalle', 'piezadetalle').
     * @param {Function} [initCallback=null] Función callback para inicializar elementos de la nueva fila (ej. Select2), recibe el elemento y las URLs.
     * @param {object} [urls=null] Objeto con las URLs de la API y el token CSRF, para pasar al initCallback si es necesario.
     */
    window.setupFormset = function(formsetId, addBtnId, emptyFormTemplateId, prefix, initCallback = null, urls = null) {
        const formsetContainer = document.getElementById(formsetId);
        const addBtn = document.getElementById(addBtnId);
        // El input oculto TOTAL_FORMS es crucial para que Django sepa cuántas filas hay
        const totalFormsInput = document.querySelector(`#${formsetId} input[name$="-TOTAL_FORMS"]`);

        // Función auxiliar para actualizar los atributos 'id' y 'name' de los elementos
        // cuando se añade o elimina una fila, manteniendo la secuencia numérica de Django (form-0-, form-1-, etc.)
        function updateElementIndex(el, currentPrefix, ndx) {
            // Expresiones regulares para encontrar y reemplazar el prefijo y el índice numérico
            const idRegex = new RegExp(`(${currentPrefix}-(\\d){1}-)`);
            const nameRegex = new RegExp(`(${currentPrefix}-(\\d){1}-)`);
            
            if (el.id) {
                el.id = el.id.replace(idRegex, `${currentPrefix}-${ndx}-`);
            }
            if (el.name) {
                el.name = el.name.replace(nameRegex, `${currentPrefix}-${ndx}-`);
            }
            // Actualizar data-select2-id si es un elemento Select2
            if (el.hasAttribute('data-select2-id')) {
                el.setAttribute('data-select2-id', el.getAttribute('data-select2-id').replace(idRegex, `${currentPrefix}-${ndx}-`));
            }
        }

        // Event listener para el botón "Añadir Fila"
        addBtn.addEventListener('click', function() {
            const currentForms = parseInt(totalFormsInput.value);
            const newFormIndex = currentForms; // El nuevo índice será el total actual
            // Obtener el HTML de la plantilla vacía y reemplazar el placeholder '__prefix__'
            const emptyFormHtml = document.getElementById(emptyFormTemplateId).innerHTML.replace(/__prefix__/g, newFormIndex);
            
            // Crear un nuevo div para la fila y añadir el HTML
            const newRow = document.createElement('div');
            newRow.className = 'formset-row row g-2 mb-3 align-items-center p-3 border rounded-3 bg-light-subtle animated-fade-in';
            newRow.innerHTML = emptyFormHtml;
            formsetContainer.appendChild(newRow);

            // Incrementar el contador total de formularios
            totalFormsInput.value = currentForms + 1;

            // Si se proporcionó un callback de inicialización (ej. para Select2), llamarlo para los elementos de la nueva fila
            if (initCallback) {
                newRow.querySelectorAll('[name]').forEach(el => {
                    // Aquí, puedes añadir lógica para determinar qué elementos necesitan inicialización
                    // Por ejemplo, solo inicializar los Select2 por su clase o tipo de nombre
                    if (el.classList.contains('descripcion-servicio-input') || el.name.endsWith('-pieza')) {
                        initCallback(el, urls); // Pasa también el objeto 'urls' al callback
                    }
                    // Si el elemento es un Select2 creado dinámicamente, debe ser inicializado.
                    // Para el caso del `<select>` de Piezas en la plantilla vacía, Select2 necesita ser llamado
                    // sobre él.
                    if (el.name.endsWith('-pieza') && !$(el).data('select2')) { // Evita reinicializar
                        initializeSelect2Pieza(el, urls); // Llama directamente la función de Select2 para piezas
                    }
                });
            }

            // Añadir evento al botón de eliminar de la nueva fila
            const removeBtn = newRow.querySelector('.remove-formset-row');
            if (removeBtn) {
                removeBtn.addEventListener('click', function() {
                    // Si es un formulario existente, marcar el campo DELETE para que Django lo elimine en el backend
                    const deleteInput = newRow.querySelector('input[name$="-DELETE"]');
                    if (deleteInput) {
                        deleteInput.checked = true;
                        newRow.style.display = 'none'; // Ocultar visualmente la fila
                    } else {
                        // Si es un formulario recién añadido, simplemente eliminarlo del DOM
                        newRow.remove();
                    }
                    // Actualizar los índices de las filas restantes
                    updateFormsetIndexes(formsetContainer, prefix);
                    // Decrementar el contador total de formularios (solo si realmente se eliminó una fila no guardada)
                    // O si se marcó para eliminación una fila existente.
                    totalFormsInput.value = parseInt(totalFormsInput.value) - 1;
                });
            }
        });

        // Función para actualizar los índices de todos los elementos en el formset
        // Se llama después de una adición o eliminación para mantener la numeración secuencial
        function updateFormsetIndexes(container, currentPrefix) {
            let index = 0;
            container.querySelectorAll('.formset-row').forEach(row => {
                const deleteInput = row.querySelector('input[name$="-DELETE"]');
                // Solo procesar filas que no están marcadas para eliminación (visibles o recién añadidas)
                if (!deleteInput || !deleteInput.checked) {
                    row.querySelectorAll('input, select, textarea').forEach(el => {
                        updateElementIndex(el, currentPrefix, index);
                    });
                    row.querySelectorAll('label').forEach(label => {
                        const forAttr = label.getAttribute('for');
                        if (forAttr) {
                            label.setAttribute('for', forAttr.replace(new RegExp(`(${currentPrefix}-(\\d){1}-)`), `${currentPrefix}-${index}-`));
                        }
                    });
                    index++;
                }
            });
        }
        
        // Configurar los botones de eliminar para las filas que ya existen al cargar la página (en modo edición)
        formsetContainer.querySelectorAll('.formset-row .remove-formset-row').forEach(removeBtn => {
            removeBtn.addEventListener('click', function() {
                const row = removeBtn.closest('.formset-row');
                const deleteInput = row.querySelector('input[name$="-DELETE"]');
                if (deleteInput) {
                    deleteInput.checked = true;
                    row.style.display = 'none'; // Ocultar visualmente la fila
                } else {
                    row.remove(); // Eliminar directamente si no es un formulario existente (sin PK)
                }
                updateFormsetIndexes(formsetContainer, prefix);
                totalFormsInput.value = parseInt(totalFormsInput.value) - 1;
            });
        });

    }; // Fin de window.setupFormset
}); // Fin de DOMContentLoaded
