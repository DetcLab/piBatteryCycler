from flask import Flask, jsonify, render_template
import time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("prueba.html")

@app.route("/valor")
def valor():
    # Ejemplo: valor dinámico (puede ser sensor, contador, etc.)
    return jsonify({
        "valor": int(time.time())  # solo como ejemplo cambiante
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)