// achilata. · todas las animaciones e interacciones del sitio
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Lenis from "lenis";
import { $, $$, pesos } from "./util.js";
import { iniciarConsentimiento } from "./consent.js";
import { iniciarPresupuesto } from "./presupuesto.js";
import { iniciarPedido } from "./pedido.js";

gsap.registerPlugin(ScrollTrigger);

const raiz = document.documentElement;
raiz.classList.add("app");
const quieto = matchMedia("(prefers-reduced-motion: reduce)").matches;
const movil = () => matchMedia("(max-width: 700px)").matches;
const pagina = document.body.dataset.pagina;
if (quieto) raiz.classList.add("sin-movimiento");

// ---------- scroll suave ----------
let lenis = null;
if (!quieto) {
  lenis = new Lenis({ lerp: 0.11, wheelMultiplier: 0.95, anchors: { offset: -90 } });
  lenis.on("scroll", ScrollTrigger.update);
  gsap.ticker.add((t) => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
}

// ---------- texto en líneas, sin innerHTML ----------
function partirLineas(el) {
  const texto = el.textContent.replace(/\s+/g, " ").trim();
  if (!texto) return [];
  el.setAttribute("aria-label", texto);
  el.textContent = "";
  const palabras = texto.split(" ").map((w) => {
    const s = document.createElement("span");
    s.textContent = w;
    s.style.display = "inline-block";
    return s;
  });
  palabras.forEach((s, i) => { el.append(s); if (i < palabras.length - 1) el.append(" "); });
  const lineas = [];
  let arriba = null;
  for (const s of palabras) {
    if (arriba === null || Math.abs(s.offsetTop - arriba) > 3) { lineas.push([]); arriba = s.offsetTop; }
    lineas[lineas.length - 1].push(s.textContent);
  }
  el.textContent = "";
  const internos = lineas.map((ws) => {
    const m = document.createElement("span");
    m.className = "linea-mascara";
    m.setAttribute("aria-hidden", "true");
    const i = document.createElement("span");
    i.textContent = ws.join(" ");
    m.append(i);
    el.append(m);
    return i;
  });
  el.classList.add("partido");
  el._texto = texto;
  return internos;
}
function restaurar(el) {
  if (!el._texto) return;
  el.textContent = el._texto;
  el.removeAttribute("aria-label");
}

function animarTitulos() {
  $$("[data-partir]:not(h1)").forEach((el) => {
    if (quieto) { el.classList.add("partido"); return; }
    const lineas = partirLineas(el);
    gsap.from(lineas, {
      yPercent: 115, rotate: 2.5, duration: 1.15, ease: "expo.out", stagger: 0.09,
      delay: el.closest(".portada") ? 0.15 : 0,
      scrollTrigger: { trigger: el, start: "top 88%", once: true },
      onComplete: () => restaurar(el),
    });
  });
}

function revelar() {
  if (quieto) return;
  $$(".revelar").forEach((el) => {
    gsap.to(el, { opacity: 1, y: 0, duration: 1.1, ease: "expo.out", delay: Number(el.dataset.retraso || 0),
      scrollTrigger: { trigger: el, start: "top 90%", once: true } });
  });
  $$(".revelar-foto").forEach((el) => {
    const img = $("img", el);
    const tl = gsap.timeline({ scrollTrigger: { trigger: el, start: "top 88%", once: true } });
    tl.to(el, { clipPath: "inset(0% 0% 0% 0% round 24px)", duration: 1.35, ease: "expo.inOut" });
    if (img) tl.to(img, { scale: 1, duration: 1.8, ease: "expo.out" }, 0.1);
  });
  $$("[data-velocidad]").forEach((el) => {
    gsap.fromTo(el, { yPercent: 0 }, { yPercent: -Number(el.dataset.velocidad) * 12, ease: "none",
      scrollTrigger: { trigger: el, start: "top bottom", end: "bottom top", scrub: true } });
  });
  $$(".goteo--abajo svg").forEach((el) => {
    gsap.fromTo(el, { scaleY: 0.15, transformOrigin: "top" }, { scaleY: 1, ease: "none",
      scrollTrigger: { trigger: el.closest(".goteo"), start: "top 95%", end: "top 35%", scrub: true } });
  });
}

function contadores() {
  $$("[data-contar]").forEach((el) => {
    const fin = Number(el.dataset.contar);
    const pref = el.dataset.prefijo ?? "";
    if (quieto) return;
    const o = { v: 0 };
    const poner = () => { el.textContent = pref + Math.round(o.v).toLocaleString("es-AR").replace(/,/g, "."); };
    gsap.to(o, { v: fin, duration: 1.1, ease: "power3.out", scrollTrigger: { trigger: el, start: "top 90%", once: true },
      onUpdate: poner, onComplete: () => { o.v = fin; poner(); } });
  });
}

// ---------- cabecera ----------
function cabecera() {
  const cab = $(".cabecera");
  if (!cab) return;
  const tonoInicial = cab.dataset.tono;
  let ultimo = 0;
  const alScroll = (y) => {
    cab.classList.toggle("con-fondo", y > 40);
    const bajando = y > ultimo && y > 300;
    cab.classList.toggle("escondida", bajando && !$(".menu-movil.abierto"));
    ultimo = y;
  };
  if (lenis) lenis.on("scroll", ({ scroll }) => alScroll(scroll));
  else addEventListener("scroll", () => alScroll(scrollY), { passive: true });

  // el tono de la cabecera sigue a la sección que tiene debajo
  $$("[data-tono]").forEach((sec) => {
    if (sec === cab) return;
    ScrollTrigger.create({
      trigger: sec, start: "top 40px", end: "bottom 40px",
      onToggle: (s) => { if (s.isActive) cab.dataset.tono = sec.dataset.tono; },
      onLeaveBack: (s) => { if (s.trigger === $$("[data-tono]")[1]) cab.dataset.tono = tonoInicial; },
    });
  });

  // menú del celular
  const menu = $(".menu-movil");
  const abrir = $(".abrir-menu"), cerrar = $(".menu-movil .cerrar");
  if (!menu || !abrir) return;
  const poner = (si) => {
    menu.classList.toggle("abierto", si);
    menu.inert = !si;
    abrir.setAttribute("aria-expanded", String(si));
    if (si) { lenis?.stop(); cerrar.focus(); } else { lenis?.start(); abrir.focus(); }
  };
  menu.inert = true;
  abrir.addEventListener("click", () => poner(true));
  cerrar.addEventListener("click", () => poner(false));
  menu.addEventListener("keydown", (e) => { if (e.key === "Escape") poner(false); });
}

function flotante() {
  const f = $(".flotante"), pie = $(".pie");
  if (!f || !pie) return;
  // aparece después de la primera pantalla, para no tapar los botones de la portada, y se va en el pie
  const poner = () => {
    const y = lenis ? lenis.scroll : scrollY;
    const enPie = pie.getBoundingClientRect().top < innerHeight;
    f.classList.toggle("escondido", y < innerHeight * 0.6 || enPie);
  };
  if (lenis) lenis.on("scroll", poner); else addEventListener("scroll", poner, { passive: true });
  poner();
}

// ---------- 3D ----------
/** El 3D solo se carga si el equipo tiene aceleración gráfica real. Si no, queda la foto. */
function hayWebGL() {
  try { if (sessionStorage.getItem("achilata_3d") === "forzar") return true; } catch { /* nada */ }
  try {
    const c = document.createElement("canvas");
    const gl = c.getContext("webgl2") || c.getContext("webgl");
    if (!gl) return false;
    const info = gl.getExtension("WEBGL_debug_renderer_info");
    const placa = String(info ? gl.getParameter(info.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER));
    gl.getExtension("WEBGL_lose_context")?.loseContext();
    return !/swiftshader|llvmpipe|softpipe|software|basic render/i.test(placa);
  } catch { return false; }
}

/** Espera la primera interacción, o unos segundos después de cargar, para no frenar la primera pantalla. */
function cuandoInteractue(ms = 3500) {
  return new Promise((listo) => {
    const eventos = ["pointermove", "pointerdown", "touchstart", "wheel", "keydown", "scroll"];
    let hecho = false;
    const ir = () => {
      if (hecho) return;
      hecho = true;
      eventos.forEach((e) => removeEventListener(e, ir, true));
      ("requestIdleCallback" in window ? requestIdleCallback : setTimeout)(() => listo(), { timeout: 600 });
    };
    eventos.forEach((e) => addEventListener(e, ir, { capture: true, passive: true, once: true }));
    const despues = () => setTimeout(ir, ms);
    if (document.readyState === "complete") despues(); else addEventListener("load", despues, { once: true });
  });
}

async function cargarPote(contenedor, opciones) {
  const sinTresD = () => { if (contenedor?.classList.contains("escena")) raiz.classList.add("sin-3d"); return null; };
  if (!contenedor || !hayWebGL()) return sinTresD();
  // el pote es lo principal del inicio: se arma apenas termina de cargar la página
  await cuandoInteractue(contenedor.classList.contains("escena") ? 150 : 3500);
  try {
    const { montarPote } = await import("./cup.js");
    const pote = await montarPote(contenedor, { logo: "assets/img/logo-rojo.svg", ...opciones });
    if (!pote) return sinTresD();
    contenedor.classList.add("con-3d");
    if (contenedor.classList.contains("escena")) raiz.classList.add("con-3d");
    ScrollTrigger.refresh();
    return pote;
  } catch (e) {
    console.warn("No se pudo cargar el 3D", e);
    return sinTresD();
  }
}

async function inicio() {
  const escena = $(".escena");
  const cargador = $(".cargador");
  let visto = false;
  try { visto = sessionStorage.getItem("achilata_visto") === "1"; } catch { /* sin almacenamiento */ }
  // el CSS hace subir cada .linea; el scroll mueve su máscara, así las dos animaciones no se pisan
  const lineas = $$(".heroe__titulo .linea-mascara");

  // cargador con porcentaje, solo la primera vez de la sesión y nunca más de un segundo y medio
  if (!visto && cargador && !quieto) {
    const numero = $(".cargador__numero", cargador);
    const progreso = { v: 0 };
    lenis?.stop();
    gsap.to(progreso, { v: 100, duration: 1.1, ease: "power2.inOut", onUpdate: () => { numero.textContent = Math.round(progreso.v); },
      onComplete: () => { cargador.classList.add("listo"); lenis?.start(); } });
  } else if (cargador) {
    cargador.classList.add("listo");
  }
  try { sessionStorage.setItem("achilata_visto", "1"); } catch { /* nada */ }
  // el título sube con CSS; acá solo se suma el texto de abajo
  if (!quieto) gsap.from(".heroe__pie > *", { opacity: 0, y: 30, duration: 1.2, ease: "expo.out", stagger: 0.1, delay: visto ? 0.45 : 1.5 });

  // sin 3D todavía, el título igual se abre al bajar
  const abrir = quieto ? null : gsap.to(lineas, { xPercent: (i) => (i % 2 ? 30 : -30), ease: "none", scrollTrigger: { trigger: ".heroe", start: "top top", end: "bottom top", scrub: 1 } });
  // el 3D se arma aparte y entra cuando está listo
  const pote = await cargarPote(escena, {});
  if (pote && abrir) { abrir.scrollTrigger.kill(); abrir.kill(); }
  if (pote && quieto) {
    pote.estado.giroAuto = 0;
    Object.assign(pote.estado, movil() ? { y: 0.42, escala: 0.84 } : { x: 1.75, y: 0.62, escala: 0.98 });
    pote.renderizar();
  } else if (pote) {
    coreografia(pote, lineas, visto ? 0 : 0.6);
  }

  // la frase de presentación se ilumina palabra por palabra
  const frase = $(".intro__frase");
  if (frase && !quieto) {
    const texto = frase.textContent.replace(/\s+/g, " ").trim();
    frase.textContent = "";
    const palabras = texto.split(" ").map((w, i, a) => {
      const s = document.createElement("span");
      s.className = "p";
      s.textContent = w;
      frase.append(s);
      if (i < a.length - 1) frase.append(" ");
      return s;
    });
    gsap.to(palabras, { opacity: 1, y: 0, stagger: 0.05, ease: "power1.out",
      scrollTrigger: { trigger: ".intro", start: "top 55%", end: "bottom 85%", scrub: true } });
  }

  // la banda de eventos: la foto se abre hasta ocupar toda la pantalla
  const marco = $(".apertura__marco");
  if (marco && !quieto) {
    const tl = gsap.timeline({ scrollTrigger: { trigger: ".apertura", start: "top top", end: "bottom bottom", scrub: true } });
    tl.fromTo(marco, { clipPath: movil() ? "inset(28% 10% 28% 10% round 24px)" : "inset(22% 31% 22% 31% round 32px)" },
      { clipPath: "inset(0% 0% 0% 0% round 0px)", ease: "none", duration: 1 })
      .fromTo(".apertura__marco img", { scale: 1.25 }, { scale: 1, ease: "none", duration: 1 }, 0)
      .fromTo(".apertura__velo", { opacity: 0 }, { opacity: 0.38, ease: "none", duration: 0.5 }, 0.5)
      .fromTo(".apertura__texto > *", { opacity: 0, y: 60 }, { opacity: 1, y: 0, stagger: 0.08, duration: 0.4, ease: "power2.out" }, 0.55);
  }
}

// La posición del pote sale siempre de la posición del scroll, con una función pura:
// así no hay animaciones que se pisen ni valores que queden a mitad de camino,
// y al volver arriba el pote está exactamente donde empezó.
const PI = Math.PI;
const POSES = {
  grande: [
    { p: 0, x: 1.75, y: 0.62, escala: 0.98, giroY: 0, giroX: 0.12, visible: 1 },
    { p: 0.5, x: 0, y: 0.8, escala: 1.15, giroY: PI * 0.8, giroX: 0.45, visible: 1 },
    { p: 1, x: 1.75, y: 0.6, escala: 0.92, giroY: PI * 1.5, giroX: 0.22, visible: 1 },
    { p: 2, x: 1.75, y: 0.6, escala: 0.92, giroY: PI * 1.5, giroX: 0.22, visible: 1 },
    { p: 3, x: 1.75, y: 3.2, escala: 0.92, giroY: PI * 2.5, giroX: 0.22, visible: 0 },
  ],
  // en el celular el pote sube pegado al héroe, así nunca se monta sobre el texto; acá y es un extra
  chico: [
    { p: 0, x: 0, y: 0, escala: 0.84, giroY: 0, giroX: 0.12, visible: 1 },
    { p: 0.3, x: 0, y: 0, escala: 0.81, giroY: PI * 0.55, giroX: 0.26, visible: 1 },
    { p: 0.62, x: 0, y: 0, escala: 0.76, giroY: PI * 1.1, giroX: 0.42, visible: 0 },
  ],
};
const suave = (t) => t * t * (3 - 2 * t);
function pose(lista, p) {
  if (p <= lista[0].p) return lista[0];
  for (let i = 1; i < lista.length; i++) {
    const a = lista[i - 1], b = lista[i];
    if (p <= b.p) {
      const t = suave((p - a.p) / (b.p - a.p || 1));
      const r = {};
      for (const k in a) r[k] = a[k] + (b[k] - a[k]) * t;
      return r;
    }
  }
  return lista[lista.length - 1];
}

function coreografia(pote, lineas, demora) {
  const e = pote.estado;
  const base = e.giroY;
  const heroe = $(".heroe"), intro = $(".intro");
  // marcas en píxeles de scroll; se miden solo cuando cambia el ancho, no cuando el celular esconde la barra
  let marcas = [0, 1, 2, 3], ancho = 0, altoEscena = 800;
  const medir = () => {
    altoEscena = $(".escena").clientHeight || innerHeight;
    const alto = heroe.offsetHeight;
    const vh = document.documentElement.clientHeight;
    const finIntro = intro ? intro.offsetTop + intro.offsetHeight : alto * 2;
    marcas = [0, alto, Math.max(finIntro - vh, alto + 1), Math.max(finIntro - vh * 0.3, alto + 2)];
    ancho = innerWidth;
  };
  medir();
  addEventListener("resize", () => { if (innerWidth !== ancho) medir(); }, { passive: true });
  ScrollTrigger.addEventListener("refresh", medir);
  const progreso = (y) => {
    if (y <= marcas[1]) return y / marcas[1];
    if (y <= marcas[2]) return 1 + (y - marcas[1]) / (marcas[2] - marcas[1]);
    return 2 + Math.min((y - marcas[2]) / (marcas[3] - marcas[2]), 1);
  };
  const entrada = { y: 6, giro: -4 };
  gsap.to(entrada, { y: 0, giro: 0, duration: 2, ease: "expo.out", delay: demora });
  let actual = null;
  gsap.ticker.add((_t, dt) => {
    const y = lenis ? lenis.scroll : scrollY;
    const chico = movil();
    const objetivo = { ...pose(chico ? POSES.chico : POSES.grande, progreso(Math.max(y, 0))) };
    // unidades del mundo por píxel de pantalla, con la cámara del celular a 11,5 y 30 grados de apertura
    if (chico) objetivo.y = 0.42 + Math.min(Math.max(y, 0), marcas[1]) * (2 * 11.5 * Math.tan(PI / 12)) / altoEscena;
    if (!actual) actual = { ...objetivo };
    // suavizado con el tiempo real del cuadro, igual en 60 y en 120 Hz
    const k = 1 - Math.exp(-Math.min(dt, 100) / 110);
    for (const c in objetivo) actual[c] += (objetivo[c] - actual[c]) * k;
    e.x = actual.x;
    e.y = actual.y + entrada.y;
    e.escala = actual.escala;
    e.giroX = actual.giroX;
    e.giroY = base + actual.giroY + entrada.giro;
    e.visible = Math.min(Math.max(actual.visible, 0), 1);
  });
  // el título se abre a los costados al bajar del héroe
  gsap.to(lineas, { xPercent: (i) => (i % 2 ? 30 : -30), ease: "none",
    scrollTrigger: { trigger: ".heroe", start: "top top", end: "bottom top", scrub: 0.6 } });
}

function laAchilata() {
  cargarPote($(".visor"), { arrastrable: true }).then((pote) => {
    if (pote) Object.assign(pote.estado, { y: 0.45, escala: 1.25 });
    if (pote && quieto) { pote.estado.giroAuto = 0; pote.renderizar(); }
    if (pote && !quieto) gsap.from(pote.estado, { escala: 0.4, giroY: -3, duration: 1.8, ease: "expo.out" });
  });
  // galería horizontal: la pista se desplaza mientras la sección queda fija
  const hor = $(".horizontal"), pista = $(".horizontal__pista");
  if (hor && pista && !quieto) {
    const distancia = () => Math.max(pista.scrollWidth - innerWidth, 0);
    gsap.to(pista, { x: () => -distancia(), ease: "none",
      scrollTrigger: { trigger: hor, start: "top top", end: () => "+=" + distancia(), pin: true, scrub: 1, invalidateOnRefresh: true, anticipatePin: 1 } });
  }
}

function eventos() {
  if (quieto) return;
  const mm = gsap.matchMedia();
  mm.add("(min-width: 701px)", () => {
    const tarjetas = $$(".paquete");
    tarjetas.forEach((t, i) => {
      const sig = tarjetas[i + 1];
      if (!sig) return;
      gsap.to(t, { scale: 0.93, ease: "none", scrollTrigger: { trigger: sig, start: "top bottom", end: "top 20%", scrub: true } });
    });
  });
  const linea = $(".pasos__linea");
  if (linea) gsap.fromTo(linea, { scaleY: 0 }, { scaleY: 1, ease: "none", scrollTrigger: { trigger: ".pasos", start: "top 70%", end: "bottom 60%", scrub: true } });
}

// ---------- arranque ----------
function arrancar() {
  cabecera();
  flotante();
  animarTitulos();
  revelar();
  contadores();
  iniciarConsentimiento();
  iniciarPresupuesto();
  iniciarPedido();
  if (pagina === "inicio") inicio();
  if (pagina === "achilata") laAchilata();
  if (pagina === "eventos") eventos();
  $$("[data-anio]").forEach((el) => { el.textContent = String(new Date().getFullYear()); });
  document.fonts?.ready.then(() => ScrollTrigger.refresh());
  addEventListener("load", () => ScrollTrigger.refresh());
}
arrancar();

export { pesos };
