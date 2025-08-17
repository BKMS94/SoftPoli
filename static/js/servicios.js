document.addEventListener("DOMContentLoaded", function () {
    // ==================== SERVICIOS ====================
    const addServicioBtn = document.getElementById("add-requerimiento-servicio");
    const servicioFormsetContainer = document.getElementById("requerimiento-servicios-formset");
    const emptyFormServicio = document.querySelector(".empty-form-servicio .formset-row");
    const totalFormsServicio = document.querySelector("#id_serviciodetalle-TOTAL_FORMS");

    if (addServicioBtn && servicioFormsetContainer && emptyFormServicio && totalFormsServicio) {
        addServicioBtn.addEventListener("click", function (e) {
            e.preventDefault();

            const formIndex = parseInt(totalFormsServicio.value, 10);
            const newFormHtml = emptyFormServicio.outerHTML.replace(/__prefix__/g, formIndex);

            servicioFormsetContainer.insertAdjacentHTML("beforeend", newFormHtml);
            totalFormsServicio.value = formIndex + 1;
        });

        servicioFormsetContainer.addEventListener("click", function (e) {
            if (e.target.closest(".remove-formset-row")) {
                e.preventDefault();
                const row = e.target.closest(".formset-row");
                const deleteInput = row.querySelector("input[type='checkbox'][name$='-DELETE']");

                if (deleteInput) {
                    // Caso: fila proveniente de BD
                    deleteInput.checked = true;
                    row.style.display = "none";
                } else {
                    // Caso: fila nueva -> eliminar nodo completo
                    row.remove();
                    totalFormsServicio.value = parseInt(totalFormsServicio.value, 10) - 1;
                }
            }
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
                    // Caso: fila proveniente de BD
                    deleteInput.checked = true;
                    row.style.display = "none";
                } else {
                    // Caso: fila nueva -> eliminar nodo completo
                    row.remove();
                    totalFormsPieza.value = parseInt(totalFormsPieza.value, 10) - 1;
                }
            }
        });
    }
});
