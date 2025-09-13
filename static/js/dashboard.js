const serviciosPorMesLabels = JSON.parse(document.getElementById('servicios_por_mes_labels').textContent);
const serviciosPorMesData = JSON.parse(document.getElementById('servicios_por_mes_data').textContent);
const vehiculosLabels = JSON.parse(document.getElementById('vehiculos_labels').textContent);
const vehiculosData = JSON.parse(document.getElementById('vehiculos_data').textContent);

// Gráfico lineal de servicios finalizados por mes
new Chart(document.getElementById('serviciosLine'), {
    type: 'line',
    data: {
        labels: serviciosPorMesLabels,
        datasets: [{
            label: 'Servicios Finalizados',
            data: serviciosPorMesData,
            borderColor: '#0d6efd',
            backgroundColor: 'rgba(13,110,253,0.1)',
            fill: true,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: false } }
    }
});

// Gráfico de pastel de vehículos por estado
new Chart(document.getElementById('vehiculosPie'), {
    type: 'pie',
    data: {
        labels: vehiculosLabels,
        datasets: [{
            data: vehiculosData,
            backgroundColor: ['#198754', '#dc3545', '#ffc107'],
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { position: 'bottom' } }
    }
});