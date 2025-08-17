// --- Lógica para formset de piezas en Servicios ---
document.addEventListener("DOMContentLoaded", function () {
    const addBtnMovimiento = document.getElementById("add-movimiento-btn");
    const tableMovimientos = document.getElementById("movimientos-table");
    const emptyRowMovimiento = document.getElementById("empty-form-row");
    const totalFormsMovimiento = document.querySelector('input[name$="-TOTAL_FORMS"]');

    if (!addBtnMovimiento || !tableMovimientos || !emptyRowMovimiento || !totalFormsMovimiento) {
        return; // si falta algo, no ejecutar
    }

    // 👉 Añadir nueva fila de pieza
    addBtnMovimiento.addEventListener("click", function (e) {
        e.preventDefault();
        const formIdx = parseInt(totalFormsMovimiento.value);
        let newRowHtml = emptyRowMovimiento.innerHTML.replace(/__prefix__/g, formIdx);
        let newRow = document.createElement("tr");
        newRow.innerHTML = newRowHtml;
        newRow.removeAttribute("id");
        newRow.style.display = "";
        tableMovimientos.querySelector("tbody").appendChild(newRow);
        totalFormsMovimiento.value = formIdx + 1;
        attachRemoveEvents();
        setTimeout(actualizarStockEnFilas, 100);
    });

    // 👉 Eliminar fila de pieza
    function attachRemoveEvents() {
        tableMovimientos.querySelectorAll(".remove-row").forEach(function (btn) {
            btn.onclick = function (e) {
                e.preventDefault();
                if (!confirm("¿Estás seguro de eliminar esta pieza?")) return;
                let row = btn.closest("tr");
                let checkbox = row.querySelector('input[type=checkbox][name$="-DELETE"]');
                if (checkbox) checkbox.checked = true; // marcar para eliminar en backend
                row.style.display = "none"; // ocultar en frontend
            };
        });
    }

    // 👉 Actualizar stock cuando se selecciona pieza
    function actualizarStockEnFilas() {
        document.querySelectorAll("#movimientos-table tbody tr").forEach(function (row) {
            const selectPieza = row.querySelector("select");
            const stockSpan = row.querySelector(".stock-info");
            if (selectPieza && stockSpan) {
                selectPieza.onchange = function () {
                    const piezaId = this.value;
                    if (piezaId) {
                        fetch(`/piezas/stock/${piezaId}/`)
                            .then((response) => response.json())
                            .then((data) => {
                                stockSpan.textContent = "(Stock: " + data.stock + ")";
                            })
                            .catch(() => {
                                stockSpan.textContent = "(Stock: -)";
                            });
                    } else {
                        stockSpan.textContent = "(Stock: -)";
                    }
                };
                if (selectPieza.value) {
                    selectPieza.dispatchEvent(new Event("change")); // refrescar stock si ya está seleccionada
                }
            }
        });
    }

    // Inicializar eventos en filas existentes
    attachRemoveEvents();
    actualizarStockEnFilas();
});

// --- Inicializar Select2 para piezas ---
window.initializeSelect2Pieza = function (element, searchUrl) {
    $(element).select2({
        minimumInputLength: 2,
        placeholder: "Busca o selecciona una pieza...",
        ajax: {
            url: searchUrl,
            dataType: "json",
            delay: 250,
            data: function (params) {
                return { q: params.term };
            },
            processResults: function (data) {
                return { results: data.results };
            },
            cache: true,
        },
    });
};
