// Preferencias de privacidad. La web no usa cookies de publicidad ni de seguimiento.
// La elección se guarda solo en este navegador, por 12 meses, y se puede cambiar desde el pie.
import { $, guardar, leer } from "./util.js";

const CLAVE = "achilata_privacidad";
const VERSION = 1;
const DOCE_MESES = 365 * 24 * 60 * 60 * 1000;

export function preferencias() {
  const p = leer(CLAVE);
  if (!p || p.v !== VERSION || Date.now() - p.fecha > DOCE_MESES) return null;
  return p;
}

/** Para sumar una herramienta opcional en el futuro: solo se carga si la persona la aceptó. */
export function permite(categoria) {
  const p = preferencias();
  return Boolean(p && p[categoria]);
}

export function iniciarConsentimiento() {
  const caja = $("#cookies");
  if (!caja) return;
  const prefs = $("#cookies-preferencias", caja);
  const medicion = $("#pref-medicion", caja);
  const btnConfig = $("[data-cookies='configurar']", caja);

  const cerrar = () => { caja.hidden = true; };
  const elegir = (medir) => {
    guardar(CLAVE, { v: VERSION, necesarias: true, medicion: Boolean(medir), fecha: Date.now() });
    cerrar();
    document.dispatchEvent(new CustomEvent("privacidad:cambio"));
  };
  const abrir = (detalle = false, enfocar = true) => {
    const p = preferencias();
    medicion.checked = Boolean(p && p.medicion);
    prefs.hidden = !detalle;
    btnConfig.textContent = detalle ? "Guardar elección" : "Configurar";
    btnConfig.setAttribute("aria-expanded", String(detalle));
    caja.hidden = false;
    // al entrar a la web no se roba el foco: solo cuando la persona abre el panel
    if (enfocar) (detalle ? medicion : $("[data-cookies='aceptar']", caja)).focus({ preventScroll: true });
  };

  $("[data-cookies='aceptar']", caja).addEventListener("click", () => elegir(true));
  $("[data-cookies='rechazar']", caja).addEventListener("click", () => elegir(false));
  btnConfig.addEventListener("click", () => {
    if (prefs.hidden) abrir(true); else elegir(medicion.checked);
  });
  caja.addEventListener("keydown", (e) => { if (e.key === "Escape" && preferencias()) cerrar(); });
  document.querySelectorAll("[data-abrir-cookies]").forEach((b) => b.addEventListener("click", () => abrir(true)));

  if (!preferencias()) abrir(false, false);
}
