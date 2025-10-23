document.getElementById("form-reserva").addEventListener("submit", async (e) => {
  e.preventDefault();

  const servicio = document.getElementById("servicio").value;
  const fecha = document.getElementById("fecha").value;
  const estado = document.getElementById("estado");

  if (!servicio || !fecha) {
    estado.textContent = "Por favor selecciona servicio y fecha.";
    estado.style.color = "red";
    return;
  }

  // Verificar disponibilidad
  const resp = await fetch("/comprobar_disponibilidad", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ servicio, fecha })
  });

  const data = await resp.json();

  if (data.disponible) {
    estado.textContent = "Disponible ✅";
    estado.style.color = "green";

    // Confirmar reserva
    await fetch("/reservar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ servicio, fecha, hora: "10:00" })
    });
    alert("Tu cita ha sido reservada correctamente 💅");
  } else {
    estado.textContent = "No disponible ❌";
    estado.style.color = "red";
  }
});
