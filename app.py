import random
from flask import Flask, render_template,url_for
from flask_socketio import SocketIO
from hardware import Ciclador

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Variable para controlar el hilo
hilo_activo = False
estado_proceso = "reposo"

c = Ciclador()

c.modo(estado_proceso)

c.config_carga.iload = 1000
c.graba_param_carga()

c.config_cargador.vreg = 4.2
c.config_cargador.ilimit = 000
c.config_cargador.ichg = 650
c.config_cargador.lowchg = False
c.config_cargador.isafe = 1250
c.config_cargador.vsafe = 4.20
print(c.graba_param_cargador())


def simulador_sensores():
    global hilo_activo
    print("Simulador iniciado...")
    
    while hilo_activo:
        # Generar valores aleatorios realistas
        # Voltaje: entre 3.0 y 4.2V
        v = c.tension()
        # Intensidad: entre 0.5 y 1.8A
        i = c.intensidad()
        # Temperatura: entre 25 y 45°C
        t = c.temperatura()
        
        # Simular un error si la temperatura sube mucho
        lista_errores = []
        if t > 40:
            lista_errores.append("Temperatura elevada")

        # ENVIAR DATOS A LA WEB
        socketio.emit('datos', {
            'tension': v,
            'intensidad': i,
            'temperatura': t
        })

        socketio.sleep(5) # Actualiza cada segundo

@socketio.on('connect')
def handle_connect():
    global hilo_activo
    if not hilo_activo:
        hilo_activo = True
        socketio.start_background_task(simulador_sensores)
        print("Hilo Activado")
        socketio.emit('estado', {
        'estado': f"SISTEMA EN {estado_proceso.upper()}", # if t < 40 else "ALERTA TÉRMICA",
        'ok': True,
        #'errores': lista_errores
    })

@socketio.on('accion')
def manejar_botones(data):
    global estado_proceso
    tipo = data.get('tipo')
    
    if tipo == 'carga':
        estado_proceso = "carga"
        print("Iniciando proceso de CARGA...")
        # Aquí llamarías a tu función de hardware: encender_rele_carga()
        
    elif tipo == 'descarga':
        estado_proceso = "descarga"
        print("Iniciando proceso de DESCARGA...")
        # Aquí: encender_rele_descarga()
        
    elif tipo == 'reposo':
        estado_proceso = "reposo"
        print("Sistema en REPOSO.")
        # Aquí: apagar_todo()
            # ENVIAR ESTADO A LA WEB
    
    print(c.modo(tipo))

    socketio.emit('estado', {
        'estado': f"SISTEMA EN {estado_proceso.upper()}", # if t < 40 else "ALERTA TÉRMICA",
        'ok': True,
        #'errores': lista_errores
    })

@socketio.on('disconnect')
def handle_disconnect():
    global hilo_activo
    hilo_activo = False
    print("Hilo desactivado")

@app.route('/')
def index():
    print(hilo_activo)
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)



