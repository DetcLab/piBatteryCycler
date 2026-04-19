const socket = io();

// Generar tabla de 10 pasos
const cuerpoCiclos = document.getElementById("cuerpoCiclos");
for (let i = 1; i <= 10; i++) {
  const fila = document.createElement("tr");
  fila.innerHTML = `
    <td style="color: #6b7280; font-weight: bold;">#${i}</td>
    <td><select class="ciclo-modo"><option value="reposo">Reposo</option><option value="carga">Carga</option><option value="descarga">Descarga</option></select></td>
    <td><input type="number" class="ciclo-i" value="0.00" step="0.01"></td>
    <td><input type="number" class="ciclo-v" value="4.20" step="0.01"></td>
    <td><input type="number" class="ciclo-t" value="5"></td>
  `;
  cuerpoCiclos.appendChild(fila);
}

// Configuración de Gráfica con eje de 0 a 4.4V
const ctx = document.getElementById("grafica").getContext('2d');
const chart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [],
    datasets: [
      { label: "Tension", borderColor: '#4fc3f7', data: [], yAxisID: 'yV', tension: 0.2, pointRadius: 0 },
      { label: "Intensidad", borderColor: '#66bb6a', data: [], yAxisID: 'yA', tension: 0.2, pointRadius: 0 },
      { label: "Temperatura", borderColor: '#ff7043', borderDash: [5, 5], data: [], yAxisID: 'yT', tension: 0.2, pointRadius: 0 }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    scales: {
      yV: {
        type: 'linear',
        position: 'left',
        min: 0,
        max: 4.4,
        title: {
          display: true,
          text: 'Tensión (V)',
          color: '#4fc3f7',
          font: { size: 20, weight: 'bold' } // <-- Tamaño título V
        },
        ticks: {
          color: '#ffffff',
          font: { size: 14 } // <-- Tamaño números V
        },
        grid: { color: '#1f2937' }
      },
      yA: {
        type: 'linear',
        position: 'right',
        min: 0,
        max: 2.0,
        title: {
          display: true,
          text: 'Intensidad (A)',
          color: '#66bb6a',
          font: { size: 20, weight: 'bold' } // <-- Tamaño título A
        },
        ticks: {
          color: '#ffffff',
          font: { size: 14 } // <-- Tamaño números A
        },
        grid: { drawOnChartArea: false }
      },
      yT: {
        type: 'linear',
        position: 'right',
        min: 0,
        max: 80,
        display: false, // Mantener oculto pero funcional
        grid: { drawOnChartArea: false }
      },
      x: {
        ticks: {
          color: '#ffffff',
          font: { size: 12 } // <-- Tamaño hora
        }
      }
    },
    plugins: {
      legend: {
        labels: {
          color: 'white',
          font: { size: 14 } // <-- Tamaño leyenda superior
        }
      }
    }
  }
});

socket.on("datos", (data) => {
  document.getElementById("tension").innerText = data.tension.toFixed(2) + " V";
  document.getElementById("intensidad").innerText = data.intensidad.toFixed(3) + " A";
  document.getElementById("temperatura").innerText = data.temperatura.toFixed(1) + " °C";

  const t = new Date().toLocaleTimeString();
  chart.data.labels.push(t);
  chart.data.datasets[0].data.push(data.tension);
  chart.data.datasets[1].data.push(data.intensidad);
  chart.data.datasets[2].data.push(data.temperatura);

  if (chart.data.labels.length > 40) {
    chart.data.labels.shift();
    chart.data.datasets.forEach(d => d.data.shift());
  }
  chart.update();
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

function accion(tipo) {socket.emit("accion", { tipo });}
function guardarConfig() { alert("Configuración guardada."); }
function guardarCiclos() { alert("Secuencia cargada."); }
