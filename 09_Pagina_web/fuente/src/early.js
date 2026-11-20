// Se carga primero y sin demora: marca que hay JavaScript para preparar las animaciones.
(function () {
  var r = document.documentElement;
  r.classList.add("js");
  if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) r.classList.add("sin-movimiento");
  // si el script principal no arranca, se muestra todo sin animaciones
  setTimeout(function () { if (!r.classList.contains("app")) r.classList.remove("js"); }, 5000);
  try { if (sessionStorage.getItem("achilata_visto") === "1") r.classList.add("sin-cargador"); } catch (e) { /* sin almacenamiento */ }
})();
