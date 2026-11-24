// Calculadora de presupuesto para eventos. Calcula en el navegador y manda todo armado por WhatsApp.
// No guarda ni envía datos a ningún servidor.
import { datos, pesos, limpiar, abrirWhatsApp, codigo, $, $$ } from "./util.js";

const TIPOS = {
  casamiento: { texto: "Casamiento", paquete: "fiesta" },
  quince: { texto: "Fiesta de 15", paquete: "fiesta" },
  empresa: { texto: "Evento de empresa", paquete: "empresa" },
  cumple: { texto: "Cumpleaños o reunión", paquete: "cumple" },
  club: { texto: "Club o torneo", paquete: "club" },
  otro: { texto: "Otro evento", paquete: "clasico" },
};
const PUBLICO = "publico";

const paquete = (id) => datos.paquetes.find((p) => p.id === id);
const fechaLarga = (iso) => {
  const [a, m, d] = iso.split("-").map(Number);
  return new Date(a, m - 1, d).toLocaleDateString("es-AR", { weekday: "long", day: "numeric", month: "long", year: "numeric" });
};
const isoLocal = (f) => `${f.getFullYear()}-${String(f.getMonth() + 1).padStart(2, "0")}-${String(f.getDate()).padStart(2, "0")}`;

/** El mismo cálculo que 08_Eventos/03_Servicio_y_precios/cotizador.py, sin los números internos. */
export function calcular({ id, invitados, horasExtra, zona, fecha }) {
  if (id === PUBLICO) return { publico: true };
  const p = paquete(id);
  let base, descuento = 0, cobrados = invitados;
  if (p.precioCerrado) {
    base = p.precioCerrado + Math.max(0, invitados - p.incluidos) * p.extra;
  } else {
    cobrados = Math.max(invitados, p.minimo);
    descuento = (datos.descuentos.find((d) => invitados >= d.desde)?.porcentaje ?? 0) / 100;
    base = cobrados * p.porInvitado * (1 - descuento);
  }
  const horaExtra = horasExtra * (invitados > 150 ? datos.horaExtra.masDe150 : datos.horaExtra.hasta150);
  const z = datos.zonas.find((x) => x.id === zona);
  const aCotizar = z.costo === null;
  const traslado = z.costo ?? 0;
  const especial = Boolean(fecha) && datos.recargoFechas.fechas.includes(fecha.slice(5));
  const sinRecargo = base + horaExtra + traslado;
  const recargo = especial ? sinRecargo * (datos.recargoFechas.porcentaje / 100) : 0;
  const total = sinRecargo + recargo;
  return {
    p, base, descuento, cobrados, horaExtra, traslado, aCotizar, recargo, total,
    sena: total * (datos.sena / 100), porInvitado: total / Math.max(invitados, 1), horas: p.horas + horasExtra,
  };
}

export function iniciarPresupuesto() {
  const form = $("#form-presupuesto");
  if (!form) return;
  const ref = codigo("AE");
  $("#r-codigo").textContent = ref;

  const rango = $("#invitados-rango"), numero = $("#invitados");
  const horas = $("#horas-extra"), fecha = $("#fecha"), zona = $("#zona");
  const estado = $("#estado-presupuesto");

  const minima = new Date();
  minima.setDate(minima.getDate() + datos.anticipacionMinimaDias);
  fecha.min = isoLocal(minima);
  const maxima = new Date();
  maxima.setFullYear(maxima.getFullYear() + 2);
  fecha.max = isoLocal(maxima);

  // paquete desde la dirección, por ejemplo eventos.html?paquete=fiesta#presupuesto
  const pedido = new URLSearchParams(location.search).get("paquete");
  if (pedido && (paquete(pedido) || pedido === PUBLICO)) {
    const r = form.querySelector(`input[name="paquete"][value="${CSS.escape(pedido)}"]`);
    if (r) r.checked = true;
  }

  // las tarjetas de paquetes eligen el paquete y bajan a la calculadora sin recargar
  $$("[data-elegir]").forEach((a) => a.addEventListener("click", (e) => {
    const r = form.querySelector(`input[name="paquete"][value="${CSS.escape(a.dataset.elegir)}"]`);
    if (!r) return;
    e.preventDefault();
    r.checked = true;
    r.dispatchEvent(new Event("change", { bubbles: true }));
    $("#presupuesto").scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  }));

  const leerForm = () => ({
    tipo: form.tipo.value,
    id: form.paquete.value,
    invitados: Math.min(Math.max(parseInt(numero.value, 10) || 0, 0), 2000),
    horasExtra: Math.min(Math.max(parseInt(horas.value, 10) || 0, 0), 4),
    zona: Number(zona.value) || 1,
    fecha: /^\d{4}-\d{2}-\d{2}$/.test(fecha.value) ? fecha.value : "",
  });

  const poner = (sel, texto) => { const el = $(sel); if (el) el.textContent = texto; };
  const fila = (sel, visible) => { const el = $(sel); if (el) el.hidden = !visible; };

  function actualizar() {
    const v = leerForm();
    const r = calcular(v);
    const publico = Boolean(r.publico);
    $$(".solo-cerrado").forEach((el) => { el.hidden = publico; });
    $$(".solo-publico").forEach((el) => { el.hidden = !publico; });
    if (publico) {
      poner("#r-paquete", "Venta al público");
      poner("#r-monto", "Sin costo");
      poner("#r-monto-nota", `Vendemos cada vasito a ${pesos(datos.ventaPublico.vasito)} y el ${datos.ventaPublico.comisionClub} % de lo vendido queda para el club u organizador.`);
      return;
    }
    poner("#r-paquete", `${r.p.nombre}, ${String(r.horas).replace(".", ",")} horas`);
    poner("#r-invitados", r.p.precioCerrado
      ? `${v.invitados}, con ${r.p.incluidos} incluidos`
      : v.invitados < r.p.minimo ? `${v.invitados}, se cobra el mínimo de ${r.p.minimo}` : String(v.invitados));
    poner("#r-servicio", pesos(r.base));
    fila("#f-descuento", r.descuento > 0);
    poner("#r-descuento", `${Math.round(r.descuento * 100)} % aplicado`);
    fila("#f-horas", r.horaExtra > 0);
    poner("#r-horas", pesos(r.horaExtra));
    poner("#r-traslado", r.aCotizar ? "A cotizar" : r.traslado ? pesos(r.traslado) : "Incluido");
    fila("#f-recargo", r.recargo > 0);
    poner("#r-recargo", pesos(r.recargo));
    poner("#r-monto", pesos(r.total));
    poner("#r-monto-nota", r.aCotizar
      ? "Más el traslado a la Zona 3, que cotizamos aparte."
      : `Seña para reservar: ${pesos(r.sena)}. Sale ${pesos(r.porInvitado)} por invitado.`);
  }

  // rango y número van sincronizados
  rango.addEventListener("input", () => { numero.value = rango.value; actualizar(); });
  numero.addEventListener("input", () => { rango.value = Math.min(Math.max(numero.value, rango.min), rango.max); actualizar(); });

  // al elegir el tipo de evento sugerimos un paquete
  $$('input[name="tipo"]', form).forEach((r) => r.addEventListener("change", () => {
    const sug = TIPOS[r.value]?.paquete;
    const opcion = sug && form.querySelector(`input[name="paquete"][value="${sug}"]`);
    if (opcion) opcion.checked = true;
    actualizar();
  }));

  $$("[data-paso]", form).forEach((b) => b.addEventListener("click", () => {
    const n = Math.min(Math.max((parseInt(horas.value, 10) || 0) + Number(b.dataset.paso), 0), 4);
    horas.value = n;
    actualizar();
  }));
  form.addEventListener("input", actualizar);
  form.addEventListener("change", actualizar);

  function error(campo, mensaje) {
    const caja = campo.closest(".campo");
    const salida = caja?.querySelector(".error");
    caja?.classList.toggle("con-error", Boolean(mensaje));
    campo.setAttribute("aria-invalid", mensaje ? "true" : "false");
    if (salida) salida.textContent = mensaje;
    return !mensaje;
  }

  function validar() {
    const v = leerForm();
    const nombre = $("#nombre");
    const ok = [
      error(nombre, limpiar(nombre.value, 60).length < 2 ? "Escribí tu nombre para saber a quién respondemos." : ""),
      error(numero, v.invitados < 1 ? "Poné cuántos invitados esperan." : ""),
      error(fecha, !v.fecha ? "Elegí la fecha del evento."
        : v.fecha < fecha.min ? `Necesitamos al menos ${datos.anticipacionMinimaDias} días de anticipación. Si es antes, escribinos igual.`
          : v.fecha > fecha.max ? "Elegí una fecha dentro de los próximos dos años." : ""),
    ];
    const primero = form.querySelector('[aria-invalid="true"]');
    if (primero) primero.focus();
    return ok.every(Boolean);
  }

  function mensaje() {
    const v = leerForm();
    const r = calcular(v);
    const z = datos.zonas.find((x) => x.id === v.zona);
    const hora = /^\d{2}:\d{2}$/.test($("#hora").value) ? `, a las ${$("#hora").value}` : "";
    const lineas = [
      "Hola achilata. Quiero pedir un presupuesto para un evento.",
      "",
      `Código: ${ref}`,
      `Nombre: ${limpiar($("#nombre").value, 60)}`,
      `Evento: ${TIPOS[v.tipo]?.texto ?? "Evento"}`,
      `Fecha: ${fechaLarga(v.fecha)}${hora}`,
      `Invitados: ${v.invitados}`,
      `Zona: ${z.nombre}, ${z.lugares}`,
    ];
    const lugar = limpiar($("#lugar").value, 80);
    if (lugar) lineas.push(`Lugar: ${lugar}`);
    if (r.publico) {
      lineas.push("Servicio: venta al público por vasito", "", "Quiero saber si pueden venir y qué necesitan del club u organizador.");
    } else {
      lineas.push(`Paquete: ${r.p.nombre}, ${String(r.horas).replace(".", ",")} horas`);
      if (v.horasExtra) lineas.push(`Horas extra: ${v.horasExtra}`);
      lineas.push("", r.aCotizar ? `Estimado de la web: ${pesos(r.total)} más el traslado a la Zona 3` : `Estimado de la web: ${pesos(r.total)}`);
      if (!r.aCotizar) lineas.push(`Seña del ${datos.sena} %: ${pesos(r.sena)}`);
    }
    const comentario = limpiar($("#comentario").value, 400);
    if (comentario) lineas.push("", `Comentarios: ${comentario}`);
    return lineas.join("\n");
  }

  $("#enviar-presupuesto").addEventListener("click", () => {
    if (!validar()) { estado.textContent = "Revisá los datos marcados para poder enviar el presupuesto."; return; }
    abrirWhatsApp(mensaje(), 0);
    estado.textContent = `Listo. Abrimos WhatsApp con tu presupuesto ${ref}. Te respondemos lo antes posible.`;
  });
  $("#copiar-presupuesto").addEventListener("click", async () => {
    if (!validar()) { estado.textContent = "Revisá los datos marcados."; return; }
    try { await navigator.clipboard.writeText(mensaje()); estado.textContent = "Copiamos el presupuesto. Pegalo donde quieras."; }
    catch { estado.textContent = "Tu navegador no dejó copiar. Usá el botón de WhatsApp."; }
  });
  $("#imprimir-presupuesto").addEventListener("click", () => print());
  form.addEventListener("submit", (e) => { e.preventDefault(); $("#enviar-presupuesto").click(); });

  actualizar();
}
