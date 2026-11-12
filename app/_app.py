"""
Monitor y control de una celda de litio.

Ejecutar:
    pip install flask
    python app.py
Abrir: http://127.0.0.1:5000

Ahora mismo la celda es una simulación (acelerada ×SIM_ACEL para que se vea
cargar y descargar en segundos). Para usar hardware real, edita SOLO las dos
funciones marcadas con "HARDWARE REAL" y pon SIM_ACEL = 1.
"""
import random
import threading
import time
from collections import deque

from flask import Flask, jsonify, render_template, request
from firmware.picycler import Ciclador

c = Ciclador()

c.modo("paro")

#c.config_carga.iload = 450
#c.config_carga.voff = 3.0
#print(c.graba_param_carga())

# c.config_cargador.vreg = 4.2
# c.config_cargador.ilimit = 000
#c.config_cargador.ichg = 650
c.config_cargador.lowchg = False
# c.config_cargador.isafe = 1250
# c.config_cargador.vsafe = 4.20
# c.config_cargador.iterm = 50
#print(c.graba_param_cargador())

app = Flask(__name__)

# ----------------------------- Configuración -------------------------------
MAX_PUNTOS = 120      # muestras que se guardan para las gráficas
PERIODO = 1.0         # segundos entre muestras
SIM_ACEL = 60         # velocidad de la simulación (1 = tiempo real)
CAPACIDAD_AH = 3.0    # capacidad de la celda simulada
R_INT = 0.05          # resistencia interna simulada (ohmios)
T_AMB = 25.0          # temperatura ambiente simulada (°C)

# Rango permitido para cada ajuste: (mínimo, máximo)
LIMITES = {
    "i_carga": (0.1, 10.0),      # A
    "i_descarga": (0.1, 10.0),   # A
    "vmax": (3.5, 4.44),         # V
    "vmin": (2.5, 3.6),          # V
}

# ------------------------------- Estado ------------------------------------
lock = threading.RLock()
historial = deque(maxlen=MAX_PUNTOS)
ctrl = {
    "modo": "paro",        # "carga" | "descarga" | "paro"
    "motivo": "",          # texto del último paro automático
    "i_carga": 1.0,
    "i_descarga": 1.0,
    "vmax": 4.20,
    "vmin": 3.00,
}
sim = {"soc": 0.5, "temp": T_AMB}

# Secuencia de hasta 10 pasos: cada uno con modo, intensidad y duración
MAX_PASOS = 10
seq = {"activa": False, "pasos": [], "idx": 0, "restante": 0.0, "aviso": ""}


# ------------------------- HARDWARE REAL (editar) ---------------------------
def aplicar_consigna(modo, corriente):
    """
    Envía la orden a tu cargador / carga electrónica / driver.
    `corriente` va en amperios: positiva = carga, negativa = descarga, 0 = paro.
    En la simulación no hace nada.
    """
    c.modo(modo)
    return


def leer_sensores(corriente_orden, dt):
    """
    Devuelve (tension_V, intensidad_A, temperatura_C).
    Con hardware real: lee tu sensor (INA219/INA226, ADC, Arduino por serie...)
    y devuelve las tres magnitudes; ignora `corriente_orden` y `dt`.
    """
    tension = c.tension()
    intensidad = c.intensidad()
    temperatura = c.temperatura()
    # --- Simulación de la celda ---
    # dt_sim = dt * SIM_ACEL
    # sim["soc"] = min(1.0, max(0.0, sim["soc"] + corriente_orden * dt_sim / 3600 / CAPACIDAD_AH))
    # ocv = 3.0 + 1.2 * sim["soc"]                      # 3.0 V vacía, 4.2 V llena
    # tension = ocv + corriente_orden * R_INT + random.uniform(-0.004, 0.004)
    # calor = corriente_orden ** 2 * R_INT              # W disipados
    # sim["temp"] += dt * (0.6 * calor - 0.02 * (sim["temp"] - T_AMB))
    # intensidad = corriente_orden + random.uniform(-0.01, 0.01) * (1 if corriente_orden else 0)
    # temperatura = sim["temp"] + random.uniform(-0.05, 0.05)
    return tension, intensidad, temperatura
# ---------------------------------------------------------------------------


def aplicar_paso():
    """Pone en marcha el paso actual de la secuencia."""
    paso = seq["pasos"][seq["idx"]]
    ctrl["modo"] = paso["modo"]
    ctrl["motivo"] = ""
    if paso["modo"] == "carga":
        ctrl["i_carga"] = paso["corriente"]
    elif paso["modo"] == "descarga":
        ctrl["i_descarga"] = paso["corriente"]
    seq["restante"] = paso["tiempo"]


def avanzar_secuencia(dt):
    """Descuenta tiempo al paso actual y salta al siguiente cuando acaba."""
    if not seq["activa"]:
        return
    seq["restante"] -= dt
    if seq["restante"] > 0:
        return
    seq["idx"] += 1
    if seq["idx"] >= len(seq["pasos"]):
        seq["activa"] = False
        ctrl["modo"], ctrl["motivo"] = "paro", ""
        seq["aviso"] = (seq["aviso"] + " · " if seq["aviso"] else "") + "Secuencia terminada"
    else:
        aplicar_paso()


def estado():
    with lock:
        return {
            "secuencia": {
                "activa": seq["activa"],
                "paso": seq["idx"] + 1 if seq["activa"] else 0,
                "total": len(seq["pasos"]),
                "restante": round(max(0.0, seq["restante"]), 1),
                "aviso": seq["aviso"],
            },
            "modo": ctrl["modo"],
            "motivo": ctrl["motivo"],
            "ajustes": {k: ctrl[k] for k in LIMITES},
            "nivel": round(sim["soc"] * 100, 1),   # solo significativo en simulación
        }


def muestrear(dt):
    """Un ciclo: aplica la orden, lee sensores y vigila los límites."""
    with lock:
        avanzar_secuencia(dt)
        modo = ctrl["modo"]
        orden = {"carga": ctrl["i_carga"], "descarga": -ctrl["i_descarga"], "paro": 0.0}[modo]
        aplicar_consigna(modo, orden)
        v, i, temp = leer_sensores(orden, dt)

        # Protecciones: si se pasa un límite, paro automático
        if modo == "carga" and v >= ctrl["vmax"]:
            ctrl["modo"], ctrl["motivo"] = "paro", f"Tensión máxima alcanzada ({ctrl['vmax']:.2f} V)"
        elif modo == "descarga" and v <= ctrl["vmin"]:
            ctrl["modo"], ctrl["motivo"] = "paro", f"Tensión mínima alcanzada ({ctrl['vmin']:.2f} V)"
        elif modo == "carga" and sim["soc"] >= 1.0:
            ctrl["modo"], ctrl["motivo"] = "paro", "Celda llena"
        elif modo == "descarga" and sim["soc"] <= 0.0:
            ctrl["modo"], ctrl["motivo"] = "paro", "Celda vacía"
        if ctrl["modo"] == "paro" and modo != "paro":
            aplicar_consigna("paro", 0.0)
            if seq["activa"]:          # un corte por protección salta al paso siguiente
                seq["aviso"] = f"Paso {seq['idx'] + 1} cortado: {ctrl['motivo']}"
                seq["restante"] = 0

        historial.append({
            "t": time.strftime("%H:%M:%S"),
            "tension": v,
            "intensidad": i,
            "temperatura": temp,
        })


def bucle():
    ultimo = time.time()
    while True:
        time.sleep(PERIODO)
        ahora = time.time()
        muestrear(ahora - ultimo)
        ultimo = ahora


# -------------------------------- Rutas ------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/datos")
def datos():
    with lock:
        return jsonify({
            "actual": historial[-1] if historial else None,
            "historial": list(historial),
            "estado": estado(),
        })


@app.route("/api/control", methods=["POST"])
def control():
    d = request.get_json(silent=True) or {}
    with lock:
        for clave, (minimo, maximo) in LIMITES.items():
            if clave in d:
                try:
                    ctrl[clave] = round(min(maximo, max(minimo, float(d[clave]))), 3)
                except (TypeError, ValueError):
                    pass
        if ctrl["vmin"] >= ctrl["vmax"]:          # la mínima siempre por debajo de la máxima
            ctrl["vmin"] = round(ctrl["vmax"] - 0.1, 3)
        if d.get("modo") in ("carga", "descarga", "paro"):
            ctrl["modo"] = d["modo"]
            ctrl["motivo"] = ""
            seq["activa"] = False      # el control manual cancela la secuencia
            seq["aviso"] = ""
        return jsonify(estado())


@app.route("/api/secuencia", methods=["POST"])
def secuencia():
    """Recibe {"accion": "iniciar", "pasos": [{modo, corriente, tiempo}]} o {"accion": "detener"}.
    `tiempo` va en segundos."""
    d = request.get_json(silent=True) or {}
    with lock:
        if d.get("accion") == "iniciar":
            pasos = []
            for p in (d.get("pasos") or [])[:MAX_PASOS]:
                try:
                    if p.get("modo") not in ("carga", "descarga", "paro"):
                        continue
                    pasos.append({
                        "modo": p["modo"],
                        "corriente": min(10.0, max(0.1, float(p.get("corriente", 1)))),
                        "tiempo": min(7 * 24 * 3600.0, max(1.0, float(p["tiempo"]))),
                    })
                except (TypeError, ValueError, KeyError):
                    continue
            if pasos:
                seq.update(activa=True, pasos=pasos, idx=0, aviso="")
                aplicar_paso()
        elif d.get("accion") == "detener":
            if seq["activa"]:
                seq["activa"] = False
                seq["aviso"] = "Secuencia detenida"
                ctrl["modo"], ctrl["motivo"] = "paro", ""
        return jsonify(estado())


if __name__ == "__main__":
    muestrear(0)                                   # primera muestra para no empezar vacío
    threading.Thread(target=bucle, daemon=True).start()
    app.run(debug=True, use_reloader=False, host='0.0.0.0')
