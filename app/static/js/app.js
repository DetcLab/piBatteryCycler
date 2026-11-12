// ---- Acceso al servidor Flask ----
const FUENTE = '';   // texto opcional delante de la última lectura
const api = {
  async datos() { const r = await fetch('/api/datos'); return r.json(); },
  async control(body) {
    const r = await fetch('/api/control', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    return r.json();
  },
  async secuencia(body) {
    const r = await fetch('/api/secuencia', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    return r.json();
  }
};

const $ = id => document.getElementById(id);
const css = getComputedStyle(document.documentElement);
const col = n => css.getPropertyValue(n).trim();
const C = { v: col('--v'), i: col('--i'), t: col('--t') };
const ejeX = { ticks: { maxTicksLimit: 8, color: col('--muted') }, grid: { display: false } };

function linea(label, color, eje, extra = {}) {
  return Object.assign({ label, data: [], borderColor: color, backgroundColor: color, borderWidth: 2, pointRadius: 0, tension: .3, yAxisID: eje }, extra);
}
function ejeY(id, titulo, color, pos, rejilla) {
  return { id, position: pos, title: { display: true, text: titulo, color }, ticks: { color }, grid: { drawOnChartArea: rejilla, color: col('--line') } };
}

const gVI = new Chart($('g-vi'), {
  type: 'line',
  data: { labels: [], datasets: [linea('Tensión (V)', C.v, 'yV'), linea('Intensidad (A)', C.i, 'yA')] },
  options: {
    responsive: true, maintainAspectRatio: false, animation: false,
    interaction: { mode: 'index', intersect: false },
    scales: { x: ejeX, yV: ejeY('yV', 'Tensión (V)', C.v, 'left', true), yA: ejeY('yA', 'Intensidad (A)', C.i, 'right', false) }
  }
});

const gT = new Chart($('g-t'), {
  type: 'line',
  data: { labels: [], datasets: [linea('Temperatura (°C)', C.t, 'yT')] },
  options: {
    responsive: true, maintainAspectRatio: false, animation: false,
    interaction: { mode: 'index', intersect: false },
    plugins: { legend: { display: false } },
    scales: { x: ejeX, yT: ejeY('yT', 'Temperatura (°C)', C.t, 'left', true) }
  }
});

// ---- Control ----
const campos = { i_carga: $('i-carga'), i_descarga: $('i-descarga'), vmax: $('vmax'), vmin: $('vmin') };
const NOMBRE_MODO = { carga: 'Cargando', descarga: 'Descargando', paro: 'En paro' };

function leerAjustes() {
  const o = {};
  for (const k in campos) { const v = parseFloat(campos[k].value); if (!isNaN(v)) o[k] = v; }
  return o;
}

function pintarEstado(e) {
  $('modo-txt').textContent = NOMBRE_MODO[e.modo];
  $('modo-txt').dataset.modo = e.modo;
  $('nivel').textContent = 'Nivel de carga ' + e.nivel.toFixed(0) + ' %';
  $('aviso').textContent = e.motivo ? 'Paro automático: ' + e.motivo : '';
  document.querySelectorAll('.botones button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.modo === e.modo)));
  for (const k in campos) {
    if (document.activeElement !== campos[k]) campos[k].value = e.ajustes[k];
  }
  const sq = e.secuencia;
  secActiva = sq.activa;
  $('seq-estado').textContent = sq.activa ? 'Paso ' + sq.paso + ' de ' + sq.total + ' · quedan ' + fmtTiempo(sq.restante) : 'Secuencia detenida';
  if (sq.aviso || sq.activa) $('seq-aviso').textContent = sq.aviso;
  $('seq-ejecutar').disabled = sq.activa;
  $('seq-detener').disabled = !sq.activa;
  $('seq-unidad').disabled = sq.activa;
  let n = 0;   // índice entre los pasos usados, para marcar el que está en curso
  filas.forEach(f => {
    const usado = f.modo.value !== '';
    f.el.classList.toggle('activa', sq.activa && usado && ++n === sq.paso);
    ajustarFila(f);
  });
}

// ---- Secuencia (10 pasos) ----
const EJEMPLO = [['carga', 3, 20], ['paro', 1, 5], ['descarga', 2, 15], ['paro', 1, 5]];
const filas = [];
let secActiva = false;

function ajustarFila(f) {
  const modo = f.modo.value;
  f.corriente.disabled = secActiva || modo === '' || modo === 'paro';
  f.tiempo.disabled = secActiva || modo === '';
  f.modo.disabled = secActiva;
}

for (let k = 0; k < 10; k++) {
  const [m, a, t] = EJEMPLO[k] || ['', 1, 10];
  const el = document.createElement('div');
  el.className = 'fila';
  el.innerHTML = '<span class="n">' + (k + 1) + '</span>' +
    '<select aria-label="Modo del paso ' + (k + 1) + '"><option value="">Sin usar</option><option value="carga">Carga</option><option value="descarga">Descarga</option><option value="paro">Paro</option></select>' +
    '<input type="number" min="0.1" max="10" step="0.1" aria-label="Intensidad del paso ' + (k + 1) + '">' +
    '<input type="number" min="1" step="any" aria-label="Tiempo del paso ' + (k + 1) + '">';
  const [sel, inI, inT] = el.querySelectorAll('select, input');
  sel.value = m; inI.value = a; inT.value = t;
  const f = { el, modo: sel, corriente: inI, tiempo: inT };
  sel.addEventListener('change', () => ajustarFila(f));
  ajustarFila(f);
  $('seq-filas').appendChild(el);
  filas.push(f);
}

function leerSecuencia() {
  const mult = parseFloat($('seq-unidad').value);
  const pasos = [];
  for (let k = 0; k < filas.length; k++) {
    const f = filas[k];
    if (!f.modo.value) continue;
    const corriente = parseFloat(f.corriente.value), tiempo = parseFloat(f.tiempo.value) * mult;
    if (!(tiempo >= 1)) return { error: 'Paso ' + (k + 1) + ': el tiempo debe ser de al menos 1 segundo.' };
    if (f.modo.value !== 'paro' && !(corriente >= 0.1 && corriente <= 10)) return { error: 'Paso ' + (k + 1) + ': la intensidad debe estar entre 0,1 y 10 A.' };
    pasos.push({ modo: f.modo.value, corriente: f.modo.value === 'paro' ? 0 : corriente, tiempo });
  }
  if (!pasos.length) return { error: 'Elige un modo en al menos un paso.' };
  return { pasos };
}

function fmtTiempo(s) {
  s = Math.ceil(s);
  if (s >= 3600) return Math.floor(s / 3600) + ' h ' + Math.floor(s % 3600 / 60) + ' min';
  if (s >= 60) return Math.floor(s / 60) + ' min ' + (s % 60) + ' s';
  return s + ' s';
}

$('seq-ejecutar').addEventListener('click', async () => {
  const r = leerSecuencia();
  if (r.error) { $('seq-aviso').textContent = r.error; return; }
  try { pintarEstado(await api.secuencia({ accion: 'iniciar', pasos: r.pasos })); } catch (e) { $('estado').className = 'error'; }
});
$('seq-detener').addEventListener('click', async () => {
  try { pintarEstado(await api.secuencia({ accion: 'detener' })); } catch (e) { $('estado').className = 'error'; }
});

async function enviar(modo) {
  const body = leerAjustes();
  if (modo) body.modo = modo;
  try { pintarEstado(await api.control(body)); } catch (e) { $('estado').className = 'error'; }
}
document.querySelectorAll('.botones button').forEach(b => b.addEventListener('click', () => enviar(b.dataset.modo)));
Object.values(campos).forEach(c => c.addEventListener('change', () => enviar()));

// ---- Lectura periódica ----
async function actualizar() {
  try {
    const { actual, historial, estado } = await api.datos();
    if (actual) {
      $('val-v').textContent = actual.tension.toFixed(3);
      $('val-i').textContent = actual.intensidad.toFixed(3);
      $('val-i').className = 'valor ' + (actual.intensidad > 0.05 ? 'carga' : actual.intensidad < -0.05 ? 'descarga' : '');
      $('val-t').textContent = actual.temperatura.toFixed(1);

      const etiquetas = historial.map(m => m.t);
      gVI.data.labels = etiquetas;
      gVI.data.datasets[0].data = historial.map(m => m.tension);
      gVI.data.datasets[1].data = historial.map(m => m.intensidad);
      gVI.update();

      gT.data.labels = etiquetas;
      gT.data.datasets[0].data = historial.map(m => m.temperatura);
      gT.update();
      $('estado').textContent = FUENTE + 'Última lectura ' + actual.t;
    }
    pintarEstado(estado);
    $('estado').className = 'ok';
  } catch (e) {
    $('estado').textContent = 'Sin conexión con el servidor';
    $('estado').className = 'error';
  }
}

actualizar();
setInterval(actualizar, 1000);
