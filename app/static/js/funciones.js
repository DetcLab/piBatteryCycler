const socket = io();

// =========================================================================
// 1. GRAFICA PRINCIPAL: SÓLO TENSIÓN E INTENSIDAD
// =========================================================================
const ctx = document.getElementById("graficaPrincipal").getContext('2d');
const chart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [],
    datasets: [
      { label: "Tensión", borderColor: '#4fc3f7', data: [], yAxisID: 'yV', tension: 0.2, pointRadius: 0 },
      { label: "Intensidad", borderColor: '#66bb6a', data: [], yAxisID: 'yA', tension: 0.2, pointRadius: 0 }
      // <-- Se ha eliminado por completo el dataset de Temperatura de aquí
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    scales: {
      yV: {
        type: 'linear', position: 'left', min: 0, max: 4.44,
        title: { display: true, text: 'Tensión (V)', color: '#4fc3f7', font: { size: 14, weight: 'bold' } },
        ticks: { color: '#ffffff' }, grid: { color: '#1f2937' }
      },
      yA: {
        type: 'linear', position: 'right', min: -2.5, max: 2.5,
        title: { display: true, text: 'Intensidad (A)', color: '#66bb6a', font: { size: 14, weight: 'bold' } },
        ticks: { color: '#ffffff' }, grid: { drawOnChartArea: false }
      },
      x: { ticks: { color: '#ffffff', font: { size: 11 } }, grid: { color: '#1f2937' } }
    },
    plugins: { legend: { labels: { color: 'white', font: { size: 12 } } } }
  }
});

// =========================================================================
// 2. GRAFICA SECUNDARIA: SÓLO TEMPERATURA
// =========================================================================
const ctxT = document.getElementById("graficaTemperatura").getContext('2d');
const chartT = new Chart(ctxT, {
  type: "line",
  data: {
    labels: [],
    datasets: [
      { label: "Temperatura", borderColor: '#ff7043', data: [], yAxisID: 'yT', tension: 0.2, pointRadius: 0 }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    scales: {
      yT: {
        type: 'linear', position: 'left', min: 0, max: 80,
        title: { display: true, text: 'Temperatura (°C)', color: '#ff7043', font: { size: 14, weight: 'bold' } },
        ticks: { color: '#ffffff' }, grid: { color: '#1f2937' }
      },
      x: { ticks: { color: '#ffffff', font: { size: 11 } }, grid: { color: '#1f2937' } }
    },
    plugins: { legend: { labels: { color: 'white', font: { size: 12 } } } }
  }
});

// =========================================================================
// 3. RECEPCIÓN Y DISTRIBUCIÓN DE DATOS (SOCKET.IO)
// =========================================================================
socket.on("datos", (data) => {
  // Actualizar los textos informativos superiores
  document.getElementById("tension").innerText = data.tension.toFixed(2) + " V";
  document.getElementById("intensidad").innerText = data.intensidad.toFixed(3) + " A";
  document.getElementById("temperatura").innerText = data.temperatura.toFixed(1) + " °C";

  const t = new Date().toLocaleTimeString();
  
  // A) Insertar tiempo y datos en la gráfica principal (índices 0 y 1)
  chart.data.labels.push(t);
  chart.data.datasets[0].data.push(data.tension);      // dataset[0] = Tensión
  chart.data.datasets[1].data.push(data.intensidad);    // dataset[1] = Intensidad

  // B) Insertar tiempo y datos en la gráfica secundaria (índice 0 de chartT)
  chartT.data.labels.push(t);
  chartT.data.datasets[0].data.push(data.temperatura); // dataset[0] de chartT = Temperatura

  // C) Desplazamiento de ventana (Mantiene máximo 40 puntos para no saturar el navegador)
  if (chart.data.labels.length > 40) {
    chart.data.labels.shift();
    chart.data.datasets.forEach(d => d.data.shift());
  }
  
  if (chartT.data.labels.length > 40) {
    chartT.data.labels.shift();
    chartT.data.datasets.forEach(d => d.data.shift());
  }

  // Redibujar ambas gráficas con sus nuevos datos independientes
  chart.update();
  chartT.update();
});

socket.on("estado", (data) => {
  const estadoDiv = document.getElementById("estadoTexto");
  const erroresDiv = document.getElementById("errores");
  estadoDiv.innerText = data.estado;
  estadoDiv.className = "estado-valor " + (data.ok ? "ok" : "error-text");

  if (data.errores && data.errores.length > 0) {
    erroresDiv.innerHTML = data.errores.map(e => `<span class="error-text">⚠ ${e}</span>`).join('');
  } else {
    erroresDiv.innerHTML = '<span style="color: #4b5563; font-style: italic; font-size: 13px;">Sin incidencias</span>';
  }
});

setTimeout(function () {
    let el = document.getElementById("flashMessage");
    if (el) {
        el.style.display = "none";
    }
}, 3000); // 3000 ms = 3 segundos

function accion(tipo) {socket.emit("accion", { tipo });}
function guardarConfig() { alert("Configuración guardada."); }
function guardarCiclos() { alert("Secuencia cargada."); }
