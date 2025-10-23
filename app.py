from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_templates("index.html")

# Ruta de reserva
@app.route("/reserva", methods=["GET", "POST"])
def reservar():
    if request.method == "POST":
        # Datos privados
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        direccion = request.form["direccion"]

        # Datos públicos
        producto = request.form["producto"]
        dia = request.form["dia"]
        duracion = request.form["duracion"]

        # Guardar todas las citas en un archivo JSON privado
        try:
            with open("citas.json", "r") as f:
                citas = json.load(f)
        except:
            citas = []

        citas.append({
            "nombre": nombre,
            "telefono": telefono,
            "direccion": direccion,
            "producto": producto,
            "dia": dia,
            "duracion": duracion,
            "fecha_registro": str(datetime.now())
        })

        with open("citas.json", "w") as f:
            json.dump(citas, f, indent=4)

        return redirect(url_for("home"))

    return render_templates("reserva.html")

# Dashboard público (solo muestra fecha, duración y producto)
@app.route("/dashboard")
def dashboard():
    try:
        with open("citas.json", "r") as f:
            citas = json.load(f)
    except:
        citas = []

    # Crear versión pública
    citas_publicas = [{"producto": c["producto"], "dia": c["dia"], "duracion": c["duracion"]} for c in citas]

    return render_template("dashboard.html", citas=citas_publicas)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

