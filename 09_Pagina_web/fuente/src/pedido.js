// Armador de pedidos de potes. Calcula el total y manda el pedido por WhatsApp.
import { datos, pesos, limpiar, abrirWhatsApp, codigo, $, $$ } from "./util.js";

export function iniciarPedido() {
  const form = $("#form-pedido");
  if (!form) return;
  const ref = codigo("AP");
  const estado = $("#estado-pedido");
  const cantidades = datos.potes.map((p) => ({ p, input: $(`#cant-${p.id}`) }));

  const leer = () => cantidades.map(({ p, input }) => ({ p, n: Math.min(Math.max(parseInt(input.value, 10) || 0, 0), 50) }));
  function actualizar() {
    const items = leer();
    const total = items.reduce((s, { p, n }) => s + p.precio * n, 0);
    $("#pedido-total").textContent = pesos(total);
    $("#pedido-detalle").textContent = items.filter((i) => i.n).map(({ p, n }) => `${n} × ${p.nombre.toLowerCase()}`).join(" y ") || "Elegí cuántos potes querés";
  }

  $$("[data-sumar]", form).forEach((b) => b.addEventListener("click", () => {
    const input = $(`#cant-${b.dataset.sumar}`);
    input.value = Math.min(Math.max((parseInt(input.value, 10) || 0) + Number(b.dataset.paso), 0), 50);
    actualizar();
  }));
  form.addEventListener("input", actualizar);

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const items = leer().filter((i) => i.n);
    const nombre = limpiar($("#p-nombre").value, 60);
    const caja = $("#p-nombre").closest(".campo");
    const errores = [];
    if (!items.length) errores.push("Sumá al menos un pote.");
    if (nombre.length < 2) errores.push("Escribí tu nombre.");
    caja.classList.toggle("con-error", nombre.length < 2);
    $("#p-nombre").setAttribute("aria-invalid", String(nombre.length < 2));
    $("#error-pedido").textContent = errores.join(" ");
    if (errores.length) { (nombre.length < 2 ? $("#p-nombre") : cantidades[0].input).focus(); return; }

    const total = items.reduce((s, { p, n }) => s + p.precio * n, 0);
    const lineas = [
      "Hola achilata. Quiero hacer un pedido.",
      "",
      `Código: ${ref}`,
      `Nombre: ${nombre}`,
      ...items.map(({ p, n }) => `${n} × ${p.nombre}: ${pesos(p.precio * n)}`),
      `Total: ${pesos(total)}`,
      `Zona: ${limpiar(form.zona.value, 40)}`,
    ];
    const dir = limpiar($("#p-direccion").value, 100);
    if (dir) lineas.push(`Dirección o referencia: ${dir}`);
    const cuando = limpiar($("#p-cuando").value, 60);
    if (cuando) lineas.push(`Para cuándo: ${cuando}`);
    lineas.push(`Pago: ${form.pago.value === "efectivo" ? "efectivo" : "transferencia"}`);
    if (form.zona.value === "Otra zona") lineas.push("", "Mi zona no está en la lista. ¿Llegan?");
    abrirWhatsApp(lineas.join("\n"), Number(form.numero.value) || 0);
    estado.textContent = `Listo. Abrimos WhatsApp con tu pedido ${ref}.`;
  });
  actualizar();
}
