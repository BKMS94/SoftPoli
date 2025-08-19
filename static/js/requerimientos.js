document.addEventListener("DOMContentLoaded", function () {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // ==================== SERVICIOS ====================
    const addServicioBtn = document.getElementById("add-requerimiento-servicio");
    const servicioFormsetContainer = document.getElementById("requerimiento-servicios-formset");
    const emptyFormServicio = document.querySelector(".empty-form-servicio .formset-row");
    const totalFormsServicio = document.querySelector("#id_serviciodetalle-TOTAL_FORMS");

    function activarAutocompletado(input, hiddenInput) {
        let datalist = document.createElement("datalist");
        datalist.id = "dl-" + Math.random().toString(36).substring(2, 9);
        input.setAttribute("list", datalist.id);
        input.insertAdjacentElement("afterend", datalist);

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

    if (addServicioBtn && servicioFormsetContainer && emptyFormServicio && totalFormsServicio) {
        addServicioBtn.addEventListener("click", function (e) {
            e.preventDefault();
            const formIndex = parseInt(totalFormsServicio.value, 10);
            const newFormHtml = emptyFormServicio.outerHTML.replace(/__prefix__/g, formIndex);
            servicioFormsetContainer.insertAdjacentHTML("beforeend", newFormHtml);

            const newRow = servicioFormsetContainer.lastElementChild;
            const input = newRow.querySelector(".descripcion-servicio-input");
            const hiddenInput = newRow.querySelector("input[name$='detalle']");
            if (input && hiddenInput) activarAutocompletado(input, hiddenInput);

            totalFormsServicio.value = formIndex + 1;
        });

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

        // Inicializar los existentes
        document.querySelectorAll(".descripcion-servicio-input").forEach(input => {
            const hiddenInput = input.parentElement.querySelector("input[name$='detalle']");
            if (hiddenInput) activarAutocompletado(input, hiddenInput);
        });
    }

    // ==================== PIEZAS ====================
    const addPiezaBtn = document.getElementById("add-requerimiento-pieza");
    const piezaFormsetContainer = document.getElementById("requerimiento-piezas-formset");
    const emptyFormPieza = document.querySelector(".empty-form-pieza .formset-row");
    const totalFormsPieza = document.querySelector("#id_piezadetalle-TOTAL_FORMS");

    if (addPiezaBtn && piezaFormsetContainer && emptyFormPieza && totalFormsPieza) {
        addPiezaBtn.addEventListener("click", function (e) {
            e.preventDefault();
            const formIndex = parseInt(totalFormsPieza.value, 10);
            const newFormHtml = emptyFormPieza.outerHTML.replace(/__prefix__/g, formIndex);
            piezaFormsetContainer.insertAdjacentHTML("beforeend", newFormHtml);
            totalFormsPieza.value = formIndex + 1;
        });

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
});