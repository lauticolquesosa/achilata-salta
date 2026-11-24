// Página de pedidos para el enlace de la bio: potes, día y turno de entrega, zona y pago. Arma el mensaje de WhatsApp.
// Los turnos, el pedido mínimo y los días hacia adelante salen de datos.json.
import { datos, pesos, limpiar, abrirWhatsApp, codigo, $, $$ } from "./util.js";

const DIAS = ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"];
const SALTA = -3 * 3600e3; // Salta está en UTC menos 3 todo el año

/** La hora de Salta como fecha UTC, para no depender del huso del celular. Las pruebas pueden fijarla con window.__ahoraSalta. */
function ahoraSalta() {
  const ms = typeof window.__ahoraSalta === "number" ? window.__ahoraSalta : Date.now();
  return new Date(ms + SALTA);
}
const minutos = (hhmm) => { const [h, m] = hhmm.split(":").map(Number); return h * 60 + m; };

/** Turnos que se pueden elegir en un día, mirando el cierre si es hoy. */
function turnosDelDia(dia, esHoy, ahora) {
  const ya = ahora.getUTCHours() * 60 + ahora.getUTCMinutes();
  return datos.turnos.filter((t) => t.dias.includes(dia.getUTCDay()) && (!esHoy || ya < minutos(t.cierre)));
}

function nombreDia(f, i) {
  const fecha = `${DIAS[f.getUTCDay()]} ${f.getUTCDate()}/${f.getUTCMonth() + 1}`;
  if (i === 0) return `Hoy, ${fecha}`;
  if (i === 1) return `Mañana, ${fecha}`;
  return fecha[0].toUpperCase() + fecha.slice(1);
}

export function iniciarPedir() {
  const form = $("#form-pedir");
  if (!form) return;
  const ref = codigo("PD");
  const cfg = datos.pedidos;
  const cantidades = datos.potes.map((p) => ({ p, input: $(`#pd-${p.id}`) }));
  const selDia = $("#pd-dia");
  const cajaTurnos = $("#pd-turnos");
  let dias = [];

  // los días que tienen al menos un turno abierto
  function armarDias() {
    const ahora = ahoraSalta();
    const hoy = new Date(Date.UTC(ahora.getUTCFullYear(), ahora.getUTCMonth(), ahora.getUTCDate()));
    const previo = selDia.value;
    dias = [];
    for (let i = 0; i < cfg.diasAdelante + 1 && dias.length < cfg.diasAdelante; i++) {
      const f = new Date(hoy.getTime() + i * 864e5);
      const turnos = turnosDelDia(f, i === 0, ahora);
      if (turnos.length) dias.push({ f, i, turnos, valor: f.toISOString().slice(0, 10) });
    }
    selDia.replaceChildren(...dias.map((d) => {
      const o = document.createElement("option");
      o.value = d.valor; o.textContent = nombreDia(d.f, d.i);
      return o;
    }));
    if (dias.some((d) => d.valor === previo)) selDia.value = previo;
    armarTurnos();
  }

  function armarTurnos() {
    const d = dias.find((x) => x.valor === selDia.value);
    const previo = form.turno?.value;
    const lista = d ? d.turnos : [];
    cajaTurnos.replaceChildren(...lista.map((t, i) => {
      const label = document.createElement("label");
      label.className = "opcion";
      const input = document.createElement("input");
      input.type = "radio"; input.name = "turno"; input.value = t.id;
      input.checked = previo ? previo === t.id : i === 0;
      const span = document.createElement("span");
      const b = document.createElement("b"); b.textContent = t.nombre;
      const s1 = document.createElement("small"); s1.textContent = `Te llega de ${t.entrega}`;
      const s2 = document.createElement("small"); s2.textContent = d.i === 0 ? `Pedís hasta las ${t.cierre}` : t.nota;
      span.append(b, s1, s2);
      label.append(input, span);
      return label;
    }));
    if (lista.length && !form.turno?.value) cajaTurnos.querySelector("input").checked = true;
    $("#pd-sin-turno").hidden = lista.length > 0;
    actualizar();
  }

  const leer = () => cantidades.map(({ p, input }) => ({ p, n: Math.min(Math.max(parseInt(input.value, 10) || 0, 0), 50) }));
  const elegido = () => {
    const d = dias.find((x) => x.valor === selDia.value);
    const t = d && datos.turnos.find((x) => x.id === form.turno?.value);
    return d && t ? { d, t } : null;
  };

  function actualizar() {
    const items = leer();
    const total = items.reduce((s, { p, n }) => s + p.precio * n, 0);
    $("#pd-total").textContent = pesos(total);
    $("#pd-detalle").textContent = items.filter((i) => i.n).map(({ p, n }) => `${n} × ${p.nombre.toLowerCase()}`).join(" y ") || "Elegí cuántos potes querés";
    const e = elegido();
    $("#pd-cuando").textContent = e ? `${nombreDia(e.d.f, e.d.i)}, turno ${e.t.nombre.toLowerCase()} de ${e.t.entrega}` : "Elegí el día y el turno";
    $("#pd-con-caja").hidden = !(cfg.efectivoCon && form.pago.value === "efectivo");
  }

  $$("[data-mas]", form).forEach((b) => b.addEventListener("click", () => {
    const input = $(`#pd-${b.dataset.mas}`);
    input.value = Math.min(Math.max((parseInt(input.value, 10) || 0) + Number(b.dataset.paso), 0), 50);
    actualizar();
  }));
  selDia.addEventListener("change", armarTurnos);
  form.addEventListener("input", actualizar);
  form.addEventListener("change", actualizar);

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    armarDias(); // por si la página quedó abierta y algún turno cerró
    const items = leer().filter((i) => i.n);
    const potes = items.reduce((s, i) => s + i.n, 0);
    const nombre = limpiar($("#pd-nombre").value, 60);
    const dir = limpiar($("#pd-direccion").value, 100);
    const cuando = elegido();
    const errores = [];
    if (potes < cfg.minimoPotes) errores.push(cfg.minimoPotes > 1 ? `El pedido mínimo es de ${cfg.minimoPotes} potes.` : "Sumá al menos un pote.");
    if (!cuando) errores.push("Elegí el día y el turno.");
    if (dir.length < 4) errores.push("Escribí tu dirección.");
    if (nombre.length < 2) errores.push("Escribí tu nombre.");
    for (const [id, mal] of [["#pd-direccion", dir.length < 4], ["#pd-nombre", nombre.length < 2]]) {
      $(id).closest(".campo").classList.toggle("con-error", mal);
      $(id).setAttribute("aria-invalid", String(mal));
    }
    $("#error-pedir").textContent = errores.join(" ");
    if (errores.length) {
      const foco = potes < cfg.minimoPotes ? cantidades[0].input : !cuando ? selDia : dir.length < 4 ? $("#pd-direccion") : $("#pd-nombre");
      foco.focus();
      return;
    }

    const total = items.reduce((s, { p, n }) => s + p.precio * n, 0);
    const efectivo = form.pago.value === "efectivo";
    const con = limpiar($("#pd-con").value, 12).replace(/[^\d.]/g, "");
    const lineas = [
      "Hola achilata. Quiero hacer un pedido.",
      "",
      `Código: ${ref}`,
      `Nombre: ${nombre}`,
      ...items.map(({ p, n }) => `${n} × ${p.nombre}: ${pesos(p.precio * n)}`),
      `Total sin envío: ${pesos(total)}`,
      `Entrega: ${nombreDia(cuando.d.f, cuando.d.i)}, turno ${cuando.t.nombre.toLowerCase()} de ${cuando.t.entrega}`,
      `Zona: ${limpiar(form.zona.value, 40)}`,
      `Dirección: ${dir}`,
      `Pago: ${efectivo ? "efectivo" : "transferencia"}`,
    ];
    if (efectivo && cfg.efectivoCon && con) lineas.push(`Pago con: $${con}`);
    if (form.zona.value === "Otra zona") lineas.push("", "Mi zona no está en la lista. ¿Llegan?");
    abrirWhatsApp(lineas.join("\n"), Number(form.numero.value) || 0);
    $("#estado-pedir").textContent = `Listo. Abrimos WhatsApp con tu pedido ${ref}.`;
  });

  armarDias();
  // si la página queda abierta, los turnos que cierran se van sacando solos
  setInterval(armarDias, 60e3);
}
