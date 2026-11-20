// Pruebas de funcionamiento: calculadora, pedido, cookies, menú, sin movimiento y sin JavaScript.
// Uso: con el sitio servido en http://127.0.0.1:8765, correr  node probar.mjs
import puppeteer from "puppeteer-core";

const BASE = process.env.BASE || "http://127.0.0.1:8765/";
const b = await puppeteer.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true });
let fallas = 0;
const ok = (cond, msg) => { console.log((cond ? "OK    " : "FALLA ") + msg); if (!cond) fallas++; };
const espera = (ms) => new Promise((r) => setTimeout(r, ms));

async function nueva(vp = { width: 1280, height: 900 }, consent = true) {
  const ctx = await b.createBrowserContext();
  const p = await ctx.newPage();
  await p.setViewport(vp);
  const errores = [];
  p.on("pageerror", (e) => errores.push(e.message));
  p.on("console", (m) => { if (m.type() === "error") errores.push(m.text()); });
  await p.evaluateOnNewDocument((c) => {
    sessionStorage.setItem("achilata_visto", "1");
    if (c) localStorage.setItem("achilata_privacidad", JSON.stringify({ v: 1, necesarias: true, medicion: false, fecha: Date.now() }));
    window.__abiertos = [];
    window.open = (u) => { window.__abiertos.push(u); return {}; };
  }, consent);
  p.errores = errores;
  return p;
}
const texto = (p, s) => p.$eval(s, (e) => e.textContent.trim());
const poner = (p, sel, valor, evento = "input") => p.evaluate((sel, valor, evento) => {
  const el = document.querySelector(sel); el.value = valor; el.dispatchEvent(new Event(evento, { bubbles: true }));
}, sel, valor, evento);

// 1. Presupuesto: los mismos números que cotizador.py
let p = await nueva();
await p.goto(BASE + "presupuesto.html?paquete=fiesta", { waitUntil: "load" });
await poner(p, "#invitados", "120");
ok((await texto(p, "#r-monto")) === "$816.000", "Fiesta, 120 invitados, zona 1 = $816.000 → " + await texto(p, "#r-monto"));
await p.click('input[name="paquete"][value="clasico"]');
await poner(p, "#invitados", "40");
ok((await texto(p, "#r-monto")) === "$330.000", "Clásico, 40 invitados, cobra el mínimo de 60 = $330.000 → " + await texto(p, "#r-monto"));
await p.click('input[name="paquete"][value="fiesta"]');
await poner(p, "#invitados", "180");
await poner(p, "#zona", "2", "change");
await p.click('[data-paso="1"]');
ok((await texto(p, "#r-monto")) === "$1.291.080", "Fiesta, 180, zona 2, una hora extra = $1.291.080 → " + await texto(p, "#r-monto"));
await p.click('[data-paso="-1"]');
await p.click('input[name="paquete"][value="cumple"]');
await poner(p, "#invitados", "50");
await poner(p, "#zona", "1", "change");
ok((await texto(p, "#r-monto")) === "$265.000", "Cumple, 50 invitados = $265.000 → " + await texto(p, "#r-monto"));
await p.click('input[name="paquete"][value="club"]');
await poner(p, "#invitados", "300");
await poner(p, "#fecha", "2026-12-31");
ok((await texto(p, "#r-monto")) === "$1.155.000", "Club cerrado, 300, el 31/12 = $1.155.000 → " + await texto(p, "#r-monto"));
await poner(p, "#zona", "3", "change");
ok((await texto(p, "#r-traslado")) === "A cotizar", "Zona 3 muestra el traslado a cotizar");
await poner(p, "#zona", "1", "change");
await p.click('input[name="paquete"][value="publico"]');
ok((await texto(p, "#r-monto")) === "Sin costo", "Venta al público, sin costo para el organizador");

// validaciones
await p.click('input[name="paquete"][value="fiesta"]');
await poner(p, "#fecha", "");
await p.click("#enviar-presupuesto");
ok((await p.evaluate(() => window.__abiertos.length)) === 0, "Sin nombre ni fecha no envía");
ok((await p.$eval("#nombre", (e) => e.getAttribute("aria-invalid"))) === "true", "Marca el nombre como inválido");
const cerca = await p.evaluate(() => { const d = new Date(); d.setDate(d.getDate() + 2); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`; });
await poner(p, "#fecha", cerca);
await p.type("#nombre", "Lucía <b>hola</b>");
await p.evaluate(() => { const n = document.querySelector("#nombre"); n.value += String.fromCharCode(0x202e) + "x"; });
await p.click("#enviar-presupuesto");
ok((await p.evaluate(() => window.__abiertos.length)) === 0, "Fecha a menos de 7 días no envía");
await poner(p, "#fecha", "2027-01-16");
await p.click("#enviar-presupuesto");
const url = await p.evaluate(() => window.__abiertos[0] || "");
const msj = url ? new URL(url).searchParams.get("text") : "";
ok(url.startsWith("https://wa.me/5493874834041?text="), "Abre WhatsApp al número principal");
ok(msj.includes("Paquete: Fiesta") && /Código: AE\d{4}[A-Z0-9]{4}/.test(msj), "El mensaje lleva el paquete y el código");
ok(!msj.includes(String.fromCharCode(0x202e)), "El mensaje no lleva caracteres de control");
ok(p.errores.length === 0, "Presupuesto sin errores de JavaScript " + p.errores.join(" | "));
console.log("\n---- mensaje de presupuesto ----\n" + msj + "\n--------------------------------\n");
await p.close();

// 2. Pedido de potes, en celular
p = await nueva({ width: 390, height: 844, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
await p.goto(BASE + "precios.html", { waitUntil: "load" });
await p.click('[data-sumar="kg1"][data-paso="1"]');
await p.click('[data-sumar="kg05"][data-paso="1"]');
ok((await texto(p, "#pedido-total")) === "$32.000", "Dos de 1 kg y uno de medio = $32.000 → " + await texto(p, "#pedido-total"));
await p.evaluate(() => document.querySelector("#form-pedido").requestSubmit());
ok((await p.evaluate(() => window.__abiertos.length)) === 0, "Pedido sin nombre no envía");
await p.type("#p-nombre", "Juan");
await p.select("#p-numero", "1");
await p.evaluate(() => document.querySelector("#form-pedido").requestSubmit());
const u2 = await p.evaluate(() => window.__abiertos[0] || "");
ok(u2.startsWith("https://wa.me/5493874684498"), "El pedido va al segundo número, el elegido");
console.log("\n---- mensaje de pedido ----\n" + (u2 ? new URL(u2).searchParams.get("text") : "") + "\n---------------------------\n");
await p.evaluate(() => scrollTo(0, 0));
await espera(800);
await p.click(".abrir-menu");
await espera(900);
ok(await p.$eval(".menu-movil", (e) => e.classList.contains("abierto") && !e.inert), "Abre el menú del celular");
await p.keyboard.press("Escape");
await espera(300);
ok(await p.$eval(".menu-movil", (e) => !e.classList.contains("abierto") && e.inert), "Escape cierra el menú");
ok(p.errores.length === 0, "Precios sin errores de JavaScript " + p.errores.join(" | "));
await p.close();

// 3. Cookies
p = await nueva(undefined, false);
await p.goto(BASE + "index.html", { waitUntil: "load" });
await espera(1500);
ok(await p.$eval("#cookies", (e) => !e.hidden), "El aviso aparece en la primera visita");
await p.click('[data-cookies="rechazar"]');
ok(await p.$eval("#cookies", (e) => e.hidden), "Rechazar cierra el aviso");
const g = await p.evaluate(() => JSON.parse(localStorage.getItem("achilata_privacidad")));
ok(g && g.medicion === false && g.necesarias === true, "Guarda la elección sin medición");
ok((await p.evaluate(() => document.cookie)) === "", "La web no crea ninguna cookie");
await p.evaluate(() => document.querySelector("[data-abrir-cookies]").click());
ok(await p.$eval("#cookies", (e) => !e.hidden) && !(await p.$eval("#cookies-preferencias", (e) => e.hidden)), "Configurar cookies reabre el panel con las preferencias");
await p.close();

// 4. Movimiento reducido: no queda nada escondido
for (const pag of ["index.html", "eventos.html", "achilata.html"]) {
  p = await nueva();
  await p.emulateMediaFeatures([{ name: "prefers-reduced-motion", value: "reduce" }]);
  await p.goto(BASE + pag, { waitUntil: "load" });
  await espera(800);
  const ocultos = await p.$$eval(".revelar, .revelar-foto, [data-partir]", (els) => els.filter((e) => {
    const s = getComputedStyle(e); return s.opacity === "0" || s.visibility === "hidden" || s.clipPath.startsWith("inset(100%");
  }).length);
  ok(ocultos === 0, `${pag} con movimiento reducido no esconde nada (${ocultos})`);
  await p.close();
}

// 5. Sin JavaScript: el contenido se ve igual
p = await b.newPage();
await p.setJavaScriptEnabled(false);
await p.goto(BASE + "index.html", { waitUntil: "load" });
ok(await p.$eval(".heroe__titulo", (e) => getComputedStyle(e).visibility !== "hidden"), "Sin JavaScript el título se ve");
ok(await p.$eval(".cargador", (e) => getComputedStyle(e).display === "none"), "Sin JavaScript no aparece el cargador");
await p.close();

await b.close();
console.log(fallas ? `\n${fallas} FALLAS` : "\nTodo bien");
process.exit(fallas ? 1 : 0);
