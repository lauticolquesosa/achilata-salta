import datos from "./datos.json";

export { datos };

export const pesos = (n) => "$" + Math.round(n).toLocaleString("es-AR").replace(/,/g, ".");

const R = (a, b) => String.fromCharCode(a) + "-" + String.fromCharCode(b);
// caracteres de control, de ancho cero y de dirección de texto, que no tienen que llegar al mensaje
const CONTROL = new RegExp("[" + R(0, 31) + R(127, 159) + R(0x200b, 0x200f) + R(0x2028, 0x202e) + R(0x2066, 0x2069) + "]", "g");

/** Limpia un texto que escribió el visitante: sin caracteres de control y con largo máximo. */
export function limpiar(texto, max = 120) {
  return String(texto ?? "")
    .normalize("NFC")
    .replace(CONTROL, " ")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, max);
}

/** Arma el enlace oficial de WhatsApp. Solo acepta los números de la marca. */
export function enlaceWhatsApp(mensaje, indice = 0) {
  const n = datos.whatsapp[indice] ?? datos.whatsapp[0];
  const url = new URL(`https://wa.me/${n.numero}`);
  url.searchParams.set("text", mensaje.slice(0, 1800));
  return url.toString();
}

/** Abre WhatsApp una sola vez. Con noopener, window.open devuelve null aunque abra la pestaña,
 * y eso hacía que también se cargara WhatsApp en la página actual: dos destinos para un pedido. */
export function abrirWhatsApp(mensaje, indice = 0) {
  const url = enlaceWhatsApp(mensaje, indice);
  const w = window.open(url, "_blank");
  if (w) { try { w.opener = null; } catch { /* nada */ } return; }
  location.href = url;
}

/** Código corto para identificar cada pedido o presupuesto en el chat. */
export function codigo(prefijo) {
  const letras = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  const azar = new Uint32Array(4);
  crypto.getRandomValues(azar);
  const sufijo = Array.from(azar, (n) => letras[n % letras.length]).join("");
  const f = new Date();
  return `${prefijo}${String(f.getDate()).padStart(2, "0")}${String(f.getMonth() + 1).padStart(2, "0")}${sufijo}`;
}

/** 1 pote de 1 kg y 2 potes de medio kilo */
export function textoPotes(items) {
  const corto = { kg1: "1 kg", kg05: "medio kilo" };
  return items.map(({ p, n }) => `${n} ${n === 1 ? "pote" : "potes"} de ${corto[p.id] ?? p.nombre}`).join(" y ");
}

export const $ = (s, el = document) => el.querySelector(s);
export const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));

export function guardar(clave, valor) {
  try { localStorage.setItem(clave, JSON.stringify(valor)); return true; } catch { return false; }
}
export function leer(clave) {
  try { return JSON.parse(localStorage.getItem(clave)); } catch { return null; }
}
