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
        maintainAspectRatio: false, // Permite controlar el tamaño por CSS
        plugins: { 
            legend: { display: false },
            tooltip: { mode: 'index', intersect: false }
        },
        scales: {
            x: {
                ticks: {
                    maxRotation: 45,
                    minRotation: 0,
                    autoSkip: true,
                    maxTicksLimit: 6
                }
            }
        }
    }
});

// Gráfico de pastel de vehículos por estado
new Chart(document.getElementById('vehiculosPie'), {
    type: 'pie',
    data: {
        labels: vehiculosLabels,
        datasets: [{
            data: vehiculosData,
            backgroundColor: ['#198754', '#dc3545', '#6c757d','#fd7e14', '#ffc107', '#212529', '#0d6efd'],
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { 
            legend: { 
                position: 'bottom',
                labels: {
                    boxWidth: 18,
                    font: { size: 14 },
                    padding: 16
                }
            }
        }
    }
});