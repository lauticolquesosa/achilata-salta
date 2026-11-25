// achilata. · todas las animaciones e interacciones del sitio
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Lenis from "lenis";
import { $, $$, pesos } from "./util.js";
import { iniciarConsentimiento } from "./consent.js";
import { iniciarPresupuesto } from "./presupuesto.js";
import { iniciarPedido } from "./pedido.js";
import { iniciarPedir } from "./pedir.js";

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

async function inicio() {
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

  // el título se abre a los costados al bajar del héroe
  if (!quieto) gsap.to(lineas, { xPercent: (i) => (i % 2 ? 30 : -30), ease: "none", scrollTrigger: { trigger: ".heroe", start: "top top", end: "bottom top", scrub: 1 } });

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

function laAchilata() {
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
  iniciarPedir();
  if (pagina === "inicio") inicio();
  if (pagina === "achilata") laAchilata();
  if (pagina === "eventos") eventos();
  $$("[data-anio]").forEach((el) => { el.textContent = String(new Date().getFullYear()); });
  document.fonts?.ready.then(() => ScrollTrigger.refresh());
  addEventListener("load", () => ScrollTrigger.refresh());
}
arrancar();

export { pesos };
