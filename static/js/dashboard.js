const dashboardData = {
    servicios_labels: JSON.parse(document.getElementById('servicios_labels').textContent),
    servicios_data: JSON.parse(document.getElementById('servicios_data').textContent),
    vehiculos_labels: JSON.parse(document.getElementById('vehiculos_labels').textContent),
    vehiculos_data: JSON.parse(document.getElementById('vehiculos_data').textContent),
    meses: JSON.parse(document.getElementById('meses').textContent),
    tdrs_por_mes: JSON.parse(document.getElementById('tdrs_por_mes').textContent),
};

// Servicios por Estado (Bar)
new Chart(document.getElementById('serviciosBar'), {
    type: 'bar',
    data: {
        labels: dashboardData.servicios_labels,
        datasets: [{
            label: 'Servicios',
            data: dashboardData.servicios_data,
            backgroundColor: ['#ffc107', '#0d6efd', '#198754'],
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: false } }
    }
});

// Vehículos por Estado (Pie)
new Chart(document.getElementById('vehiculosPie'), {
    type: 'pie',
    data: {
        labels: dashboardData.vehiculos_labels,
        datasets: [{
            data: dashboardData.vehiculos_data,
            backgroundColor: ['#198754', '#dc3545', '#ffc107'],
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { position: 'bottom' } }
    }
});

// TDRs por Mes (Line)
new Chart(document.getElementById('tdrsLine'), {
    type: 'line',
    data: {
        labels: dashboardData.meses,
        datasets: [{
            label: 'TDRs',
            data: dashboardData.tdrs_por_mes,
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