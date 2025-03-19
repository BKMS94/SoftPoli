function calcularDiferencia() {
    var kilometrajeAct = document.getElementById("id_kilometraje_act").value;
    var kilometrajeVehiculo = document.getElementById("id_kilometraje_vehiculo").value;
    var diferencia = kilometrajeAct - kilometrajeVehiculo;
    document.getElementById("id_kilometraje_diff").value = diferencia;
}

