// Revisión automática del sitio: errores de consola, violaciones de la CSP, recursos rotos,
// desbordes horizontales, reglas de texto de la marca y capturas a lo largo del scroll.
// Uso: con el sitio servido en http://127.0.0.1:8765, correr  node revisar.mjs [carpeta-capturas]
import puppeteer from "puppeteer-core";
import { mkdirSync } from "node:fs";
import { join } from "node:path";

const BASE = process.env.BASE || "http://127.0.0.1:8765/";
const SALIDA = process.argv[2] || "capturas";
const CHROME = process.env.CHROME || "C:/Program Files/Google/Chrome/Application/chrome.exe";
const PAGINAS = ["index.html", "achilata.html", "precios.html", "pedir.html", "eventos.html", "presupuesto.html", "privacidad.html", "cookies.html", "terminos.html", "seguridad.html", "no-existe.html"];
const PANTALLAS = { escritorio: { width: 1440, height: 900, deviceScaleFactor: 1 }, celular: { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true } };
const CAPTURAS = Number(process.env.CAPTURAS || 6);
const SOLO = process.env.SOLO ? process.env.SOLO.split(",") : null;
mkdirSync(SALIDA, { recursive: true });

const navegador = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--hide-scrollbars"] });
let problemas = 0;
const reporte = [];
for (const [nombre, vp] of Object.entries(PANTALLAS)) {
  for (const pag of PAGINAS.filter((p) => !SOLO || SOLO.includes(p))) {
    const page = await navegador.newPage();
    await page.setViewport(vp);
    const avisos = [];
    page.on("console", (m) => { if (["error", "warn"].includes(m.type())) avisos.push(`consola ${m.type()}: ${m.text()}`); });
    page.on("pageerror", (e) => avisos.push("error js: " + e.message));
    page.on("requestfailed", (r) => avisos.push("falló: " + r.url() + " " + r.failure()?.errorText));
    page.on("response", (r) => { if (r.status() >= 400 && !r.url().includes("no-existe")) avisos.push(`http ${r.status()}: ${r.url()}`); });
    await page.evaluateOnNewDocument(() => {
      document.addEventListener("securitypolicyviolation", (e) => console.error(`CSP ${e.violatedDirective} ${e.blockedURI} ${e.sourceFile}:${e.lineNumber}`));
      try { sessionStorage.setItem("achilata_visto", "1"); sessionStorage.setItem("achilata_3d", "forzar"); } catch {}
      if (!window.__mostrarCookies) try { localStorage.setItem("achilata_privacidad", JSON.stringify({ v: 1, necesarias: true, medicion: false, fecha: Date.now() })); } catch {}
    });
    await page.goto(BASE + pag, { waitUntil: "networkidle0", timeout: 60000 });
    await new Promise((r) => setTimeout(r, 1800));
    const datos = await page.evaluate(() => {
      const texto = document.body.innerText;
      const prohibidos = [];
      for (const [re, n] of [[/["“”«»]/g, "comillas"], [/[—–]/g, "raya"], [/\s-\s|\w-\w/g, "guion"], [/[()]/g, "paréntesis"]]) {
        const m = texto.match(re);
        if (m) prohibidos.push(`${n}: ${[...new Set(m)].slice(0, 5).join(" ")}`);
      }
      return {
        ancho: document.documentElement.scrollWidth, vista: innerWidth, alto: document.documentElement.scrollHeight,
        tresD: document.documentElement.classList.contains("con-3d") || Boolean(document.querySelector(".visor.con-3d")),
        prohibidos, titulo: document.title, h1: document.querySelectorAll("h1").length,
        sinAlt: [...document.images].filter((i) => !i.hasAttribute("alt")).length,
      };
    });
    if (datos.ancho > datos.vista + 1) avisos.push(`desborde horizontal: ${datos.ancho} > ${datos.vista}`);
    if (datos.prohibidos.length) avisos.push("texto: " + datos.prohibidos.join(" | "));
    if (datos.h1 !== 1) avisos.push(`h1: ${datos.h1}`);
    if (datos.sinAlt) avisos.push(`imágenes sin alt: ${datos.sinAlt}`);
    // capturas a lo largo de la página
    for (let i = 0; i < CAPTURAS; i++) {
      const y = Math.round((datos.alto - vp.height) * (i / Math.max(CAPTURAS - 1, 1)));
      await page.evaluate((y) => window.scrollTo(0, y), y);
      await new Promise((r) => setTimeout(r, 1300));
      await page.screenshot({ path: join(SALIDA, `${pag.replace(".html", "")}-${nombre}-${i}.jpg`), type: "jpeg", quality: 70 });
    }
    problemas += avisos.length;
    reporte.push(`${nombre} ${pag} · 3D ${datos.tresD ? "sí" : "no"} · alto ${datos.alto}px\n${avisos.map((a) => "   " + a).join("\n") || "   sin problemas"}`);
    await page.close();
  }
}
await navegador.close();
console.log(reporte.join("\n"));
console.log(`\nTotal de avisos: ${problemas}`);
