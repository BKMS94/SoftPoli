// --- Lógica para formset de piezas en Servicios ---
document.addEventListener("DOMContentLoaded", function () {
    // --- Formset de piezas ---
    const addBtnMovimiento = document.getElementById("add-movimiento-btn");
    const tableMovimientos = document.getElementById("movimientos-table");
    const emptyRowMovimiento = document.getElementById("empty-form-row");
    const totalFormsMovimiento = document.querySelector('input[name$="-TOTAL_FORMS"]');

    if (addBtnMovimiento && tableMovimientos && emptyRowMovimiento && totalFormsMovimiento) {
        // Añadir nueva fila de pieza
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

        // Eliminar fila de pieza
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

        // Actualizar stock cuando se selecciona pieza
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
    }

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

    // --- Lógica para kilometraje en Servicios ---
    const vehiculoSelect = $('#id_vehiculo');
    const kilometrajeAnteriorInput = $('#id_kilometraje_ant, #id_kilometraje_vehiculo'); // Soporta ambos nombres
    const kilometrajeActualInput = $('#id_kilometraje_act');
    const kilometrajeDiffInput = $('#id_kilometraje_diff');

    // Inicializa select2 si no lo has hecho antes
    if (vehiculoSelect.length && !vehiculoSelect.hasClass('select2-hidden-accessible')) {
        vehiculoSelect.select2();
    }

    // Evento Select2: selecciona vehículo y busca kilometraje
    vehiculoSelect.on('select2:select', function (e) {
        const vehiculoId = e.params.data.id;
        fetch(`/vehiculos/kilometraje/${vehiculoId}/`)
            .then(response => response.json())
            .then(data => {
                kilometrajeAnteriorInput.val(data.kilometraje);
                calcularDiferencia();
            })
            .catch(error => {
                kilometrajeAnteriorInput.val(0);
                calcularDiferencia();
            });
    });

    // Función: calcular diferencia de kilometraje
    function calcularDiferencia() {
        const kmAnterior = parseFloat(kilometrajeAnteriorInput.val() || 0);
        const kmActual = parseFloat(kilometrajeActualInput.val() || 0);
        let diff = kmActual - kmAnterior;
        if (!Number.isFinite(diff)) diff = 0;
        kilometrajeDiffInput.val(Math.max(0, diff).toFixed(1));
    }

    // Evento input en campo kilometraje actual
    kilometrajeActualInput.on('input', calcularDiferencia);

    // Si ya hay un vehículo seleccionado al cargar, dispara el evento para cargar el kilometraje
    if (vehiculoSelect.val()) {
        vehiculoSelect.trigger('select2:select', {
            data: { id: vehiculoSelect.val() }
        });
    }
});
