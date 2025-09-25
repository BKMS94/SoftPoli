document.addEventListener("DOMContentLoaded", function () {
    // === CSRF Token para peticiones POST ===
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // ==================== SERVICIOS ====================
    // --- Variables para el formset de servicios ---
    const addServicioBtn = document.getElementById("add-requerimiento-servicio");
    const servicioFormsetContainer = document.getElementById("requerimiento-servicios-formset");
    const emptyFormServicio = document.querySelector(".empty-form-servicio .formset-row");
    const totalFormsServicio = document.querySelector("#id_serviciodetalle-TOTAL_FORMS");

    // --- Autocompletado para servicios ---
    function activarAutocompletado(input, hiddenInput) {
        let datalist = document.createElement("datalist");
        datalist.id = "dl-" + Math.random().toString(36).substring(2, 9);
        input.setAttribute("list", datalist.id);
        input.insertAdjacentElement("afterend", datalist);

        // Buscar servicios existentes
        input.addEventListener("input", async function () {
            const query = this.value.trim();
            if (query.length < 2) return;
            try {
                const resp = await fetch(`/tdr/api/descripciones/buscar/?q=${encodeURIComponent(query)}`);
                const data = await resp.json();
                datalist.innerHTML = "";
                data.results.forEach(opt => {
                    let option = document.createElement("option");
                    option.value = opt.text;
                    option.dataset.id = opt.id;
                    datalist.appendChild(option);
                });
            } catch (err) {
                console.error("Error buscando descripciones:", err);
            }
        });

        // Crear servicio si no existe
        input.addEventListener("change", async function () {
            const selectedOption = Array.from(datalist.options).find(o => o.value === this.value);
            if (selectedOption) {
                hiddenInput.value = selectedOption.dataset.id;
            } else {
                try {
                    const resp = await fetch(`/tdr/api/descripciones/crear/`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/x-www-form-urlencoded",
                            "X-CSRFToken": csrfToken
                        },
                        body: `descripcion=${encodeURIComponent(this.value)}`
                    });
                    const data = await resp.json();
                    if (data.id) hiddenInput.value = data.id;
                } catch (err) {
                    console.error("Error creando descripción:", err);
                }
            }
        });
    }

    // --- Añadir nueva fila de servicio ---
    if (addServicioBtn && servicioFormsetContainer && emptyFormServicio && totalFormsServicio) {
        addServicioBtn.addEventListener("click", function (e) {
            e.preventDefault();
            const formIndex = parseInt(totalFormsServicio.value, 10);
            const newFormHtml = emptyFormServicio.outerHTML.replace(/__prefix__/g, formIndex);
            servicioFormsetContainer.insertAdjacentHTML("beforeend", newFormHtml);

            const newRow = servicioFormsetContainer.lastElementChild;
            const input = newRow.querySelector(".descripcion-servicio-input");
            const hiddenInput = newRow.querySelector("input[name$='detalle_servicio']");
            if (input && hiddenInput) activarAutocompletado(input, hiddenInput);

            totalFormsServicio.value = formIndex + 1;
        });

        // Inicializar autocompletado en filas existentes
        document.querySelectorAll(".descripcion-servicio-input").forEach(input => {
            const hiddenInput = input.parentElement.querySelector("input[name$='detalle_servicio']");
            if (hiddenInput) activarAutocompletado(input, hiddenInput);
        });
    }

    // --- Eliminar fila de servicio ---
    if (servicioFormsetContainer) {
        servicioFormsetContainer.addEventListener("click", function (e) {
            if (e.target.closest(".remove-formset-row")) {
                e.preventDefault();
                const row = e.target.closest(".formset-row");
                const deleteInput = row.querySelector("input[type='checkbox'][name$='-DELETE']");
                if (deleteInput) {
                    deleteInput.checked = true;
                    row.style.display = "none";
                } else {
                    row.remove();
                    totalFormsServicio.value = parseInt(totalFormsServicio.value, 10) - 1;
                }
            }
        });
    }

    // ==================== PIEZAS ====================
    // --- Variables para el formset de piezas ---
    const addPiezaBtn = document.getElementById("add-requerimiento-pieza");
    const piezaFormsetContainer = document.getElementById("requerimiento-piezas-formset");
    const emptyFormPieza = document.querySelector(".empty-form-pieza .formset-row");
    const totalFormsPieza = document.querySelector("#id_piezadetalle-TOTAL_FORMS");

    // --- Autocompletado para piezas ---
    function activarAutocompletadoPieza(input, hiddenInput) {
        let datalist = document.createElement("datalist");
        datalist.id = "dl-pieza-" + Math.random().toString(36).substring(2, 9);
        input.setAttribute("list", datalist.id);
        input.insertAdjacentElement("afterend", datalist);

        // Buscar piezas existentes
        input.addEventListener("input", async function () {
            const query = this.value.trim();
            if (query.length < 2) return;
            try {
                const resp = await fetch(`/tdr/api/piezas/buscar/?q=${encodeURIComponent(query)}`);
                const data = await resp.json();
                datalist.innerHTML = "";
                data.results.forEach(opt => {
                    let option = document.createElement("option");
                    option.value = opt.text;
                    option.dataset.id = opt.id;
                    datalist.appendChild(option);
                });
            } catch (err) {
                console.error("Error buscando piezas:", err);
            }
        });

        // Crear pieza si no existe
        input.addEventListener("change", async function () {
            const selectedOption = Array.from(datalist.options).find(o => o.value === this.value);
            if (selectedOption) {
                hiddenInput.value = selectedOption.dataset.id;
            } else {
                try {
                    const resp = await fetch(`/tdr/api/piezas/crear/`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/x-www-form-urlencoded",
                            "X-CSRFToken": csrfToken
                        },
                        body: `pieza=${encodeURIComponent(this.value)}`
                    });
                    const data = await resp.json();
                    if (data.id) hiddenInput.value = data.id;
                } catch (err) {
                    console.error("Error creando pieza:", err);
                }
            }
        });
    }

    // --- Inicializar autocompletado en filas existentes de piezas ---
    document.querySelectorAll(".descripcion-pieza-input").forEach(input => {
        const hiddenInput = input.parentElement.querySelector("input[name$='detalle_pieza']");
        if (hiddenInput) activarAutocompletadoPieza(input, hiddenInput);
    });

    // --- Añadir nueva fila de pieza ---
    if (addPiezaBtn && piezaFormsetContainer && emptyFormPieza && totalFormsPieza) {
        addPiezaBtn.addEventListener("click", function (e) {
            e.preventDefault();
            const formIndex = parseInt(totalFormsPieza.value, 10);
            const newFormHtml = emptyFormPieza.outerHTML.replace(/__prefix__/g, formIndex);
            piezaFormsetContainer.insertAdjacentHTML("beforeend", newFormHtml);

            const newRow = piezaFormsetContainer.lastElementChild;
            const input = newRow.querySelector(".descripcion-pieza-input");
            const hiddenInput = newRow.querySelector("input[name$='detalle_pieza']");
            if (input && hiddenInput) activarAutocompletadoPieza(input, hiddenInput);

            totalFormsPieza.value = formIndex + 1;
        });

        // --- Eliminar fila de pieza ---
        piezaFormsetContainer.addEventListener("click", function (e) {
            if (e.target.closest(".remove-formset-row")) {
                e.preventDefault();
                const row = e.target.closest(".formset-row");
                const deleteInput = row.querySelector("input[type='checkbox'][name$='-DELETE']");
                if (deleteInput) {
                    deleteInput.checked = true;
                    row.style.display = "none";
                } else {
                    row.remove();
                    totalFormsPieza.value = parseInt(totalFormsPieza.value, 10) - 1;
                }
            }
        });
    }

    // ==================== LIMPIAR CAMPOS ====================
    // Permite limpiar cualquier input, select o textarea con el botón .clear-input
    document.body.addEventListener("click", function (e) {
        if (e.target.classList.contains("clear-input")) {
            const input = e.target.closest(".position-relative").querySelector("input, select, textarea");
            if (input) {
                if (input.tagName === "SELECT") {
                    input.selectedIndex = 0; // resetear select
                } else {
                    input.value = ""; // limpiar texto o número
                }
            }
        }
    });

    // === CHECKBOX SELECCIONAR TODOS ===
    const selectAllCheckbox = document.getElementById('select-all');
    const itemCheckboxes = document.querySelectorAll('.select-item');

    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            itemCheckboxes.forEach(function(checkbox) {
                checkbox.checked = selectAllCheckbox.checked;
            });
        });

        itemCheckboxes.forEach(function(checkbox) {
            checkbox.addEventListener('change', function() {
                if (!this.checked) {
                    selectAllCheckbox.checked = false;
                } else {
                    const allChecked = Array.from(itemCheckboxes).every(cb => cb.checked);
                    selectAllCheckbox.checked = allChecked;
                }
            });
        });
    }
});