// Genera el sitio en ../sitio a partir de paginas/, partes/, src/ y src/datos.json.
// Uso: npm run build
import { build } from "esbuild";
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync, readdirSync, mkdirSync, rmSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const SITIO = join(AQUI, "..", "sitio");
const datos = JSON.parse(readFileSync(join(AQUI, "src", "datos.json"), "utf8"));
const medidas = JSON.parse(readFileSync(join(AQUI, "src", "medidas.json"), "utf8"));
const D = datos.sitio.dominio;

// ---------- seguridad ----------
const CSP_BASE = [
  "default-src 'none'",
  "script-src 'self' {{hashScript}}",
  "style-src 'self' {{hashEstilo}}",
  "img-src 'self'",
  "font-src 'self'",
  "connect-src 'self'",
  "manifest-src 'self'",
  "base-uri 'none'",
  "form-action 'none'",
  "object-src 'none'",
  "upgrade-insecure-requests",
  "require-trusted-types-for 'script'",
  "trusted-types 'none'",
];
let CSP_CABECERA = [...CSP_BASE, "frame-ancestors 'none'"].join("; ");
let CSP_META = CSP_BASE.join("; ");
const CABECERAS = {
  "Content-Security-Policy": "",
  "Strict-Transport-Security": "max-age=63072000; includeSubDomains",
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "accelerometer=(), autoplay=(), camera=(), display-capture=(), encrypted-media=(), fullscreen=(self), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), midi=(), payment=(), picture-in-picture=(), publickey-credentials-get=(), screen-wake-lock=(), serial=(), usb=(), xr-spatial-tracking=(), browsing-topics=()",
  "Cross-Origin-Opener-Policy": "same-origin",
  "Cross-Origin-Resource-Policy": "same-origin",
  "Cross-Origin-Embedder-Policy": "require-corp",
  "Origin-Agent-Cluster": "?1",
  "X-Permitted-Cross-Domain-Policies": "none",
  "X-DNS-Prefetch-Control": "off",
};

// ---------- utilidades ----------
const pesos = (n) => "$" + Math.round(n).toLocaleString("es-AR").replace(/,/g, ".");
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const hash = (txt) => createHash("sha256").update(txt).digest("hex").slice(0, 10);
const tel = (n) => "+" + n;

// ---------- preguntas frecuentes, una sola fuente para la página y para Google ----------
const FAQ = {
  precios: [
    ["¿Cuánto sale la achilata?", `El pote de 1 kg sale ${pesos(datos.potes[0].precio)} y el de medio kilo, ${pesos(datos.potes[1].precio)}.`],
    ["¿Venden vasitos?", "No. A domicilio vendemos solo potes de 1 kg y de medio kilo. Los vasitos los usamos únicamente en el servicio para eventos."],
    ["¿Dónde hacen delivery?", `En ${datos.delivery.slice(0, -1).join(", ")} y ${datos.delivery.at(-1)}. Si vivís en otra zona de Salta, escribinos y vemos si llegamos.`],
    ["¿Cuánto cuesta el envío?", "Depende de la zona. Te lo decimos al confirmar el pedido por WhatsApp, antes de que pagues."],
    ["¿Cómo se paga?", "Por transferencia o en efectivo."],
    ["¿Qué sabores hay?", "Uno solo, el clásico tucumano. Es el que se toma en Tucumán de toda la vida."],
    ["¿Tiene leche?", "No. La achilata es un helado de agua."],
  ],
  eventos: [
    ["¿Con cuánta anticipación hay que reservar?", `Lo antes posible, porque los fines de semana de verano se llenan. Pedimos al menos ${datos.anticipacionMinimaDias} días y una seña del ${datos.sena} % para tomar la fecha.`],
    ["¿Qué necesitan en el lugar?", "Un espacio de dos por dos metros, plano y con acceso para el carrito. Si el servicio es de noche, un enchufe cerca."],
    ["¿Cuándo llegan?", "Una hora antes del horario contratado, para armar todo sin molestar. Al terminar dejamos el espacio limpio."],
    ["¿Y si llueve?", "Si el evento es al aire libre, nos tienen que prever un lugar techado. Si se suspende por lluvia, la seña se usa para otra fecha dentro de los 90 días."],
    ["¿Y si se termina la achilata?", "No pasa: llevamos un 20 % más de lo que calculamos para la cantidad de invitados y las horas de servicio."],
    ["¿Tiene leche?", "La achilata no tiene leche. La salsa de leche condensada del paquete Fiesta sí, y lo avisamos en el carrito."],
    ["¿Hacen factura?", "Sí, para empresas. Avisanos al pedir el presupuesto."],
    ["¿Puedo sumar horas en el momento?", `Sí, si tenemos producto. La hora extra cuesta ${pesos(datos.horaExtra.hasta150)} hasta 150 invitados y ${pesos(datos.horaExtra.masDe150)} si son más.`],
  ],
};
const faqHTML = (lista) => `<div class="preguntas">${lista.map(([p, r]) =>
  `<details class="revelar"><summary>${esc(p)}</summary><div class="respuesta"><p>${esc(r)}</p></div></details>`).join("")}</div>`;
const faqLD = (lista) => ({ "@type": "FAQPage", mainEntity: lista.map(([p, r]) => ({ "@type": "Question", name: p, acceptedAnswer: { "@type": "Answer", text: r } })) });

// ---------- fotos ----------
function foto(nombre, alt, { clase = "foto--retrato", tamanos = "(max-width: 700px) 90vw, 40vw", carga = "lazy", prioridad = "", revelar = true, velocidad = "" } = {}) {
  const m = medidas[nombre];
  if (!m) throw new Error("Foto inexistente: " + nombre);
  const w640 = Math.min(640, m.w), w1100 = Math.min(1100, m.w);
  const src = (ext) => `assets/img/${nombre}-640.${ext} ${w640}w, assets/img/${nombre}-1100.${ext} ${w1100}w`;
  const h = Math.round(m.h * w1100 / m.w);
  return `<div class="foto ${clase}${revelar ? " revelar-foto" : ""}"${velocidad ? ` data-velocidad="${velocidad}"` : ""}><picture>` +
    `<source type="image/avif" srcset="${src("avif")}" sizes="${tamanos}">` +
    `<source type="image/webp" srcset="${src("webp")}" sizes="${tamanos}">` +
    `<img src="assets/img/${nombre}-1100.webp" width="${w1100}" height="${h}" alt="${esc(alt)}" loading="${carga}" decoding="async"${prioridad ? ` fetchpriority="${prioridad}"` : ""}>` +
    `</picture></div>`;
}

// ---------- datos estructurados ----------
const negocio = {
  "@type": ["LocalBusiness", "IceCreamShop"],
  "@id": D + "/#negocio",
  name: datos.sitio.nombre,
  alternateName: datos.sitio.nombreLegal,
  description: "Achilata, el helado de agua tucumano, en Salta Capital. Potes de 1 kg y medio kilo con delivery y servicio de carrito de achilata para eventos.",
  url: D + "/",
  logo: D + "/icon-512.png",
  image: D + "/assets/img/compartir.jpg",
  telephone: tel(datos.whatsapp[0].numero),
  address: { "@type": "PostalAddress", addressLocality: "Salta", addressRegion: "Salta", addressCountry: "AR" },
  areaServed: [...datos.delivery, "Salta Capital"].map((n) => ({ "@type": "Place", name: n + ", Salta" })),
  priceRange: `${pesos(datos.potes[1].precio)} a ${pesos(datos.potes[0].precio)}`,
  currenciesAccepted: "ARS",
  paymentAccepted: "Efectivo, transferencia bancaria",
  servesCuisine: "Helado tucumano",
  sameAs: [datos.sitio.instagram],
  contactPoint: datos.whatsapp.map((w) => ({ "@type": "ContactPoint", telephone: tel(w.numero), contactType: "customer service", availableLanguage: "es" })),
};
const migas = (nombre, ruta) => ({ "@type": "BreadcrumbList", itemListElement: [
  { "@type": "ListItem", position: 1, name: "Inicio", item: D + "/" },
  { "@type": "ListItem", position: 2, name: nombre, item: `${D}/${ruta}` }] });
const LD = {
  inicio: () => [negocio, { "@type": "WebSite", "@id": D + "/#sitio", url: D + "/", name: datos.sitio.nombre, inLanguage: "es-AR", publisher: { "@id": D + "/#negocio" } }],
  achilata: () => [negocio, migas("La achilata", "achilata.html")],
  precios: () => [negocio, migas("Precios y pedidos", "precios.html"), {
    "@type": "Product", name: "Achilata, helado de agua tucumano", brand: { "@type": "Brand", name: datos.sitio.nombre },
    image: D + "/assets/img/pila-potes-1100.webp", description: "Helado de agua tucumano del sabor clásico, en potes de 1 kg y medio kilo, con delivery en Salta.",
    offers: datos.potes.map((p) => ({ "@type": "Offer", name: p.nombre, price: p.precio, priceCurrency: "ARS", availability: "https://schema.org/InStock",
      areaServed: "Salta, Argentina", seller: { "@id": D + "/#negocio" } })),
  }, faqLD(FAQ.precios)],
  eventos: () => [negocio, migas("Servicio para eventos", "eventos.html"), {
    "@type": "Service", name: "Carrito de achilata para eventos", serviceType: "Servicio de helado para eventos",
    provider: { "@id": D + "/#negocio" }, areaServed: datos.zonas.slice(0, 2).map((z) => z.lugares).join(", "),
    offers: { "@type": "AggregateOffer", priceCurrency: "ARS", lowPrice: 3500, highPrice: 6800, offerCount: datos.paquetes.length,
      description: "Precio por invitado según el paquete, con mínimo de invitados" },
  }, faqLD(FAQ.eventos)],
  presupuesto: () => [negocio, migas("Presupuesto", "presupuesto.html")],
  pedir: () => [negocio, migas("Hacer un pedido", "pedir.html")],
  privacidad: () => [migas("Política de privacidad", "privacidad.html")],
  cookies: () => [migas("Política de cookies", "cookies.html")],
  terminos: () => [migas("Términos y condiciones", "terminos.html")],
  seguridad: () => [migas("Seguridad", "seguridad.html")],
  error: () => [],
};

// ---------- goteo de la marca: una banda roja con gotas que cuelgan ----------
function goteo() {
  const gotas = [[60, 34, 62], [175, 22, 44], [262, 40, 88], [390, 26, 52], [505, 46, 96], [640, 24, 40], [735, 36, 74],
    [860, 28, 58], [985, 44, 92], [1100, 22, 46], [1205, 38, 80], [1330, 30, 60], [1410, 20, 38]];
  let d = "M0,0 H1440 V16";
  for (const [c, w, L] of [...gotas].reverse()) {
    const a = c - w / 2, b = c + w / 2, r = w / 2;
    d += ` L${b + 7},16 C${b},16 ${b},21 ${b},27 V${L - r} A${r},${r} 0 0 1 ${a},${L - r} V27 C${a},21 ${a},16 ${a - 7},16`;
  }
  d += " L0,16 Z";
  return `<svg viewBox="0 0 1440 100" preserveAspectRatio="xMidYMin slice" aria-hidden="true" focusable="false"><path fill="currentColor" d="${d}"/></svg>`;
}

// ---------- bloques que salen de los datos ----------
const horasTexto = (h) => h === 1.5 ? "90 minutos" : `${h} horas`;
const BLOQUES = {
  paquetes: () => `<div class="paquetes">${datos.paquetes.map((p) => `
<article class="paquete" aria-labelledby="paq-${p.id}">
  <div>
    <h3 class="titulo paquete__nombre" id="paq-${p.id}">${esc(p.nombre)}</h3>
    <p class="paquete__para texto-grande">${esc(p.para)}</p>
  </div>
  <div class="paquete__lado">
    <div>
      <p class="paquete__precio">${pesos(p.precioCerrado ?? p.porInvitado)}</p>
      <p class="paquete__unidad">${p.precioCerrado ? `Precio cerrado hasta ${p.incluidos} invitados` : `Por invitado, con un mínimo de ${p.minimo}`}</p>
    </div>
    <ul>${p.incluye.map((i) => `<li>${esc(i)}</li>`).join("")}</ul>
    <div class="datos-paquete chico"><span>${horasTexto(p.horas)} de servicio</span><span>${p.precioCerrado ? `Invitado extra ${pesos(p.extra)}` : `Desde ${pesos(p.porInvitado * p.minimo)}`}</span></div>
    <a class="boton" href="presupuesto.html?paquete=${p.id}">Calcular con este paquete</a>
  </div>
</article>`).join("")}</div>`,
  opcionesPaquete: () => datos.paquetes.map((p, i) => `
<label class="opcion"><input type="radio" name="paquete" value="${p.id}"${i === 0 ? " checked" : ""}><span><b>${esc(p.nombre)}</b><small>${p.precioCerrado ? `${pesos(p.precioCerrado)} hasta ${p.incluidos} invitados` : `${pesos(p.porInvitado)} por invitado, mínimo ${p.minimo}`}</small><small>${horasTexto(p.horas)}</small></span></label>`).join("") +
    `<label class="opcion"><input type="radio" name="paquete" value="publico"><span><b>Venta al público</b><small>Vasito a ${pesos(datos.ventaPublico.vasito)}, sin costo para el club</small><small>Torneos, ferias y eventos abiertos</small></span></label>`,
  opcionesZona: () => datos.zonas.map((z) => `<option value="${z.id}">${esc(z.nombre)}: ${esc(z.lugares)}</option>`).join(""),
  opcionesDelivery: () => datos.delivery.map((d) => `<option>${esc(d)}</option>`).join("") + "<option>Otra zona</option>",
  listaDelivery: () => `<ul class="lista-grande">${datos.delivery.map((d) => `<li class="revelar"><span class="nombre">${esc(d)}</span></li>`).join("")}<li class="revelar"><span class="nombre">Otra zona de Salta</span><span class="dato">Escribinos y vemos si llegamos</span></li></ul>`,
  tablaDescuentos: () => `<table class="tabla"><caption>Descuentos por cantidad</caption><thead><tr><th scope="col">Invitados</th><th scope="col">Descuento</th></tr></thead><tbody>
<tr><td>Hasta ${datos.descuentos.at(-1).desde - 1}</td><td>Precio de lista</td></tr>
${[...datos.descuentos].reverse().map((d, i, a) => `<tr><td>${a[i + 1] ? `De ${d.desde} a ${a[i + 1].desde - 1}` : `${d.desde} o más`}</td><td>${d.porcentaje} %</td></tr>`).join("")}</tbody></table>`,
  tablaTurnos: () => {
    const DIAS = ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"];
    const dias = (l) => { const o = [1, 2, 3, 4, 5, 6, 0].filter((d) => l.includes(d)); if (o.length > 2 && o.every((d, i) => i === 0 || d === (o[i - 1] + 1) % 7)) return `${DIAS[o[0]]} a ${DIAS[o.at(-1)]}`; return o.map((d) => DIAS[d]).join(" y "); };
    return `<table class="tabla"><caption>Turnos de entrega</caption><thead><tr><th scope="col">Turno</th><th scope="col">Días</th><th scope="col">Pedís hasta</th><th scope="col">Te llega</th></tr></thead><tbody>
${datos.turnos.filter((t) => t.dias.length).map((t) => `<tr><th scope="row">${esc(t.nombre)}</th><td>${esc(dias(t.dias)[0].toUpperCase() + dias(t.dias).slice(1))}</td><td>${esc(t.cierre)} del mismo día</td><td>${esc(t.entrega)}</td></tr>`).join("")}</tbody></table>`;
  },
  tablaHoras: () => `<table class="tabla"><caption>Hora extra</caption><thead><tr><th scope="col">Invitados</th><th scope="col">Por hora</th></tr></thead><tbody>
<tr><td>Hasta 150</td><td>${pesos(datos.horaExtra.hasta150)}</td></tr><tr><td>Más de 150</td><td>${pesos(datos.horaExtra.masDe150)}</td></tr></tbody></table>`,
  tablaZonas: () => `<table class="tabla"><caption>Zonas de traslado</caption><thead><tr><th scope="col">Zona</th><th scope="col">Lugares</th><th scope="col">Traslado</th></tr></thead><tbody>
${datos.zonas.map((z) => `<tr><th scope="row">${esc(z.nombre)}</th><td>${esc(z.lugares)}. ${esc(z.distancia)}</td><td>${z.costo === null ? "A cotizar" : z.costo ? pesos(z.costo) : "Incluido"}</td></tr>`).join("")}</tbody></table>`,
};

// ---------- tokens ----------
function obtener(ruta) {
  return ruta.split(".").reduce((o, k) => (o == null ? undefined : o[k]), datos);
}
function tokens(html, extra) {
  return html
    .replace(/\{\{faq:(\w+)\}\}/g, (_, k) => faqHTML(FAQ[k]))
    .replace(/\{\{goteo\}\}/g, goteo)
    .replace(/\{\{bloque:(\w+)\}\}/g, (_, k) => { if (!BLOQUES[k]) throw new Error("Bloque inexistente: " + k); return BLOQUES[k](); })
    .replace(/\{\{foto:([\w-]+)\|([^|}]*)(?:\|(\{[^}]*\}))?\}\}/g, (_, n, alt, op) => foto(n, alt, op ? JSON.parse(op) : {}))
    .replace(/\{\{([\w.]+)(?:\|(\w+))?\}\}/g, (todo, ruta, filtro) => {
      let v = ruta in extra ? extra[ruta] : obtener(ruta);
      if (v === undefined) throw new Error("Dato inexistente: " + ruta);
      if (filtro === "pesos") return pesos(v);
      if (filtro === "num") return Math.round(v).toLocaleString("es-AR").replace(/,/g, ".");
      if (filtro === "raw") return v;
      return esc(v);
    });
}

// ---------- compilación ----------
async function compilar() {
  rmSync(join(SITIO, "assets", "js"), { recursive: true, force: true });
  mkdirSync(join(SITIO, "assets", "js"), { recursive: true });
  mkdirSync(join(SITIO, "assets", "css"), { recursive: true });
  await build({
    entryPoints: { app: join(AQUI, "src", "main.js") },
    outdir: join(SITIO, "assets", "js"), bundle: true, splitting: true, format: "esm",
    minify: true, target: ["es2020", "safari15"], chunkNames: "[name]-[hash]", legalComments: "eof",
    loader: { ".json": "json" }, logLevel: "warning",
  });
  await build({
    entryPoints: [join(AQUI, "src", "early.js")], outfile: join(SITIO, "assets", "js", "early.js"),
    minify: true, target: ["es2015"], logLevel: "warning",
  });
  await build({
    entryPoints: [join(AQUI, "src", "site.css")], outfile: join(SITIO, "assets", "css", "site.css"),
    minify: true, logLevel: "warning", target: ["chrome100", "safari15", "firefox100"],
  });
}

function paginas(v) {
  const partes = {};
  for (const f of readdirSync(join(AQUI, "partes"))) partes[f.replace(".html", "")] = readFileSync(join(AQUI, "partes", f), "utf8");
  const salida = [];
  for (const f of readdirSync(join(AQUI, "paginas"))) {
    let src = readFileSync(join(AQUI, "paginas", f), "utf8");
    const m = src.match(/^<!--meta\s+([\s\S]*?)-->\s*/);
    if (!m) throw new Error("Falta meta en " + f);
    const meta = JSON.parse(m[1]);
    meta.titulo = tokens(meta.titulo, {});
    meta.descripcion = tokens(meta.descripcion, {});
    src = src.slice(m[0].length);
    const ruta = f === "index.html" ? "" : f;
    const ld = { "@context": "https://schema.org", "@graph": LD[meta.pagina]() };
    const extra = {
      titulo: meta.titulo, descripcion: meta.descripcion, canonica: `${D}/${ruta}`, pagina: meta.pagina,
      tono: meta.tono || "claro", csp: CSP_META, estilo: ESTILO, early: EARLY, base: meta.pagina === "error" ? "/" : "", vjs: v.js,
      jsonld: JSON.stringify(ld).replace(/</g, "\\u003c"), robots: meta.robots || "index, follow, max-image-preview:large",
      waPrincipal: `https://wa.me/${datos.whatsapp[0].numero}?text=${encodeURIComponent("Hola achilata. Quiero hacer un pedido.")}`,
      waSegundo: `https://wa.me/${datos.whatsapp[1].numero}?text=${encodeURIComponent("Hola achilata. Quiero hacer un pedido.")}`,
      waEventos: `https://wa.me/${datos.whatsapp[0].numero}?text=${encodeURIComponent("Hola achilata. Quiero consultar por el servicio para eventos.")}`,
      waArrepentimiento: `https://wa.me/${datos.whatsapp[0].numero}?text=${encodeURIComponent("Hola achilata. Quiero ejercer mi derecho de arrepentimiento sobre mi pedido o reserva. Mi nombre es: ")}`,
    };
    let html = src.replace(/<!--#(\w+)-->/g, (_, k) => {
      if (!(k in partes)) throw new Error("Parte inexistente: " + k);
      return partes[k];
    });
    html = tokens(html, extra);
    // marca la página actual en el menú
    html = html.replace(new RegExp(`(<a[^>]+href="${(ruta || "index.html").replace(".", "\\.")}")`, "g"), '$1 aria-current="page"');
    writeFileSync(join(SITIO, f), html);
    salida.push({ f, meta, ruta });
  }
  return salida;
}

function extras(lista) {
  const hoy = datos.sitio.actualizadoISO;
  const indexables = lista.filter((p) => !p.meta.robots?.includes("noindex"));
  const prioridad = { inicio: "1.0", precios: "0.9", pedir: "0.9", eventos: "0.9", presupuesto: "0.8", achilata: "0.8" };
  writeFileSync(join(SITIO, "sitemap.xml"),
    `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
    indexables.map((p) => `  <url><loc>${D}/${p.ruta}</loc><lastmod>${hoy}</lastmod><priority>${prioridad[p.meta.pagina] || "0.3"}</priority></url>`).join("\n") +
    `\n</urlset>\n`);
  writeFileSync(join(SITIO, "robots.txt"),
    `# achilata. · Salta\nUser-agent: *\nAllow: /\nDisallow: /404.html\n\n# Buscadores con IA: bienvenidos\nUser-agent: GPTBot\nAllow: /\nUser-agent: OAI-SearchBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: Claude-SearchBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: ${D}/sitemap.xml\n`);
  const p = datos.paquetes;
  writeFileSync(join(SITIO, "llms.txt"),
`# achilata.

> Achilata, el helado de agua tucumano, en Salta Capital, Argentina. Venta de potes con delivery y servicio de carrito de achilata para eventos. Datos vigentes al ${datos.sitio.actualizado}.

## Producto y precios
- Achilata: helado de agua tucumano, sin leche, un solo sabor, el clásico.
- Pote de 1 kg: ${pesos(datos.potes[0].precio)}.
- Pote de medio kilo: ${pesos(datos.potes[1].precio)}.
- A domicilio se venden solo potes. No hay vasitos a domicilio.
- Delivery en ${datos.delivery.join(", ")}. Otras zonas de Salta se consultan.
- Pago por transferencia o en efectivo.
- Pedidos por WhatsApp: ${datos.whatsapp.map((w) => tel(w.numero)).join(" y ")}.
${datos.pedidos.minimoPotes > 1 ? `- Pedido mínimo: ${datos.pedidos.minimoPotes} potes.
` : ""}- Turnos de entrega: ${datos.turnos.filter((t) => t.dias.length).map((t) => `${t.nombre}, de ${t.entrega}`).join("; ")}.

## Servicio para eventos
Carrito de achilata con dos personas atendiendo y achilata libre durante el horario contratado. Precios por invitado, vigentes hasta el ${datos.sitio.vigenciaEventos}:
${p.map((x) => x.precioCerrado ? `- ${x.nombre}: ${pesos(x.precioCerrado)} precio cerrado hasta ${x.incluidos} invitados, ${String(x.horas).replace(".", ",")} horas. Invitado extra ${pesos(x.extra)}.` : `- ${x.nombre}: ${pesos(x.porInvitado)} por invitado, mínimo ${x.minimo} invitados, ${x.horas} horas. ${x.para}.`).join("\n")}
- Venta al público en torneos y clubes: vasito ${pesos(datos.ventaPublico.vasito)}, dos vasitos ${pesos(datos.ventaPublico.dosVasitos)}, ${datos.ventaPublico.comisionClub} % de lo vendido para el organizador.
- Descuentos: ${datos.descuentos.map((d) => `${d.porcentaje} % desde ${d.desde} invitados`).join(", ")}.
- Reserva con seña del ${datos.sena} %.

## Páginas
- [Inicio](${D}/)
- [Qué es la achilata](${D}/achilata.html)
- [Precios](${D}/precios.html)
- [Hacer un pedido con día y turno de entrega](${D}/pedir.html)
- [Servicio para eventos](${D}/eventos.html)
- [Presupuesto para eventos](${D}/presupuesto.html)
- [Instagram](${datos.sitio.instagram})
`);
  writeFileSync(join(SITIO, "site.webmanifest"), JSON.stringify({
    name: "achilata. Helado tucumano en Salta", short_name: "achilata.", lang: "es-AR", start_url: "/", scope: "/",
    display: "standalone", background_color: "#E7364A", theme_color: "#E7364A",
    icons: [{ src: "icon-192.png", sizes: "192x192", type: "image/png" }, { src: "icon-512.png", sizes: "512x512", type: "image/png" },
      { src: "icon-512.png", sizes: "512x512", type: "image/png", purpose: "maskable" }],
  }, null, 1));
  const vence = new Date(datos.sitio.actualizadoISO);
  vence.setFullYear(vence.getFullYear() + 1);
  mkdirSync(join(SITIO, ".well-known"), { recursive: true });
  writeFileSync(join(SITIO, ".well-known", "security.txt"),
    `Contact: ${D}/seguridad.html#reportar\nContact: https://wa.me/${datos.whatsapp[0].numero}\nExpires: ${vence.toISOString()}\nPreferred-Languages: es, en\nCanonical: ${D}/.well-known/security.txt\nPolicy: ${D}/seguridad.html\n`);

  // cabeceras para Netlify y Cloudflare Pages
  const bloque = (ruta, h) => `${ruta}\n${Object.entries(h).map(([k, v]) => `  ${k}: ${v}`).join("\n")}\n`;
  writeFileSync(join(SITIO, "_headers"),
    bloque("/*", CABECERAS) +
    bloque("/assets/js/*", { "Cache-Control": "public, max-age=31536000, immutable" }) +
    bloque("/assets/css/*", { "Cache-Control": "public, max-age=31536000, immutable" }) +
    bloque("/assets/fonts/*", { "Cache-Control": "public, max-age=31536000, immutable" }) +
    bloque("/assets/img/*", { "Cache-Control": "public, max-age=2592000" }) +
    bloque("/*.html", { "Cache-Control": "public, max-age=0, must-revalidate" }) +
    bloque("/.well-known/security.txt", { "Content-Type": "text/plain; charset=utf-8" }));
  // y para Vercel
  const lista2 = (h) => Object.entries(h).map(([key, value]) => ({ key, value }));
  writeFileSync(join(SITIO, "vercel.json"), JSON.stringify({
    $schema: "https://openapi.vercel.sh/vercel.json",
    cleanUrls: false, trailingSlash: false,
    headers: [
      { source: "/(.*)", headers: lista2(CABECERAS) },
      { source: "/assets/(js|css|fonts)/(.*)", headers: [{ key: "Cache-Control", value: "public, max-age=31536000, immutable" }] },
      { source: "/assets/img/(.*)", headers: [{ key: "Cache-Control", value: "public, max-age=2592000" }] },
    ],
  }, null, 1));
}

await compilar();
// CSS y script inicial van dentro de cada página; la CSP los autoriza por su hash, sin abrir la puerta a otro código
const sha = (txt) => "'sha256-" + createHash("sha256").update(txt, "utf8").digest("base64") + "'";
const ESTILO = readFileSync(join(SITIO, "assets", "css", "site.css"), "utf8").replace(/url\(\.\.\/fonts\//g, "url(/assets/fonts/").trim();
const EARLY = readFileSync(join(SITIO, "assets", "js", "early.js"), "utf8").trim();
for (const [k, h] of [["{{hashScript}}", sha(EARLY)], ["{{hashEstilo}}", sha(ESTILO)]]) {
  CSP_CABECERA = CSP_CABECERA.replace(k, h);
  CSP_META = CSP_META.replace(k, h);
}
CABECERAS["Content-Security-Policy"] = CSP_CABECERA;
// ya van dentro de cada página: no hace falta publicarlos sueltos
rmSync(join(SITIO, "assets", "css"), { recursive: true, force: true });
rmSync(join(SITIO, "assets", "js", "early.js"), { force: true });
const v = {
  js: hash(readFileSync(join(SITIO, "assets", "js", "app.js"))),
};
const lista = paginas(v);
extras(lista);
console.log("Sitio listo:", lista.map((p) => p.f).join(", "));
if (!existsSync(join(SITIO, "assets", "img", "logo-rojo.svg"))) console.warn("Falta correr python assets.py");
