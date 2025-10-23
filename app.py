from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Archivo donde guardaremos las citas
CITAS_FILE = "data/citas.json"

# Cargar o crear archivo de citas
def cargar_citas():
    try:
        with open(CITAS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def guardar_citas(citas):
    with open(CITAS_FILE, "w") as f:
        json.dump(citas, f, indent=2)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/reserva")
def reserva():
    return render_template("reserva.html")

@app.route("/comprobar_disponibilidad", methods=["POST"])
def comprobar_disponibilidad():
    data = request.get_json()
    fecha = data["fecha"]
    servicio = data["servicio"]

    citas = cargar_citas()
    ocupadas = [c for c in citas if c["fecha"] == fecha and c["servicio"] == servicio]

    if len(ocupadas) < 5:  # máximo 5 citas por día/servicio
        return jsonify({"disponible": True})
    else:
        return jsonify({"disponible": False})

@app.route("/reservar", methods=["POST"])
def reservar():
    data = request.get_json()
    citas = cargar_citas()
    citas.append(data)
    guardar_citas(citas)
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True)
