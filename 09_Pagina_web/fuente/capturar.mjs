// Capturas de la portada del inicio a lo largo del tiempo, en celular y escritorio.
// Uso: node capturar.mjs [carpeta] [url]
import puppeteer from "puppeteer-core";
import { mkdirSync } from "node:fs";
import { join } from "node:path";

const SALIDA = process.argv[2] || "capturas";
const URL_BASE = process.argv[3] || "https://achilata-salta.vercel.app/";
mkdirSync(SALIDA, { recursive: true });
const b = await puppeteer.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: "new" });
const pantallas = [
  ["celular", { width: 390, height: 844, isMobile: true, hasTouch: true, deviceScaleFactor: 2 }, true],
  ["escritorio", { width: 1440, height: 900 }, false],
];
for (const [nombre, vp, visto] of pantallas) {
  const ctx = await b.createBrowserContext();
  const p = await ctx.newPage();
  await p.setViewport(vp);
  await p.evaluateOnNewDocument((v) => {
    localStorage.setItem("achilata_privacidad", JSON.stringify({ v: 1, necesarias: true, medicion: false, fecha: Date.now() }));
    if (v) sessionStorage.setItem("achilata_visto", "1");
  }, visto);
  await p.goto(URL_BASE + "?v=" + Date.now(), { waitUntil: "load" });
  for (const [ms, etiqueta] of [[600, "1"], [1400, "2"], [3500, "3"]]) {
    await new Promise((r) => setTimeout(r, ms));
    await p.screenshot({ path: join(SALIDA, `${nombre}-${etiqueta}.jpg`), type: "jpeg", quality: 60 });
  }
  await p.evaluate(() => scrollTo(0, innerHeight * 0.6));
  await new Promise((r) => setTimeout(r, 1500));
  await p.screenshot({ path: join(SALIDA, `${nombre}-4.jpg`), type: "jpeg", quality: 60 });
  await ctx.close();
}
await b.close();
console.log("capturas en", SALIDA);
