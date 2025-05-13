//dash/static/js/compButton.js
document.getElementById("btn-ir").addEventListener("click", function () {
  var año = document.getElementById("año").value;
  var mes = document.getElementById("mes").value;
  // Redireccionar a vista Django que procesa los parámetros
  window.location.href = `/home/comparacion/?año=${año}&mes=${mes}`;
});

document.getElementById("btn-ir2").addEventListener("click", function () {
  var año = document.getElementById("añoAnual").value;

  // Guardar el año seleccionado para la anualidad
  localStorage.setItem("añoAnualSeleccionado", año);

  // Redireccionar a vista Django que procesa los parámetros
  window.location.href = `/home/ver_comparacion_anual/?año=${año}`;
});


