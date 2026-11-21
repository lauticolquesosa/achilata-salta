// El pote de achilata en 3D. Todo es geometría generada acá: no se descarga ningún modelo.
import {
  WebGLRenderer, Scene, PerspectiveCamera, Group, Mesh,
  LatheGeometry, IcosahedronGeometry, CylinderGeometry,
  MeshPhysicalMaterial, MeshStandardMaterial, CanvasTexture, Vector2, Vector3, Color,
  DirectionalLight, HemisphereLight, PMREMGenerator, SRGBColorSpace, NeutralToneMapping,
  DoubleSide, BufferAttribute, MathUtils,
} from "three";
import { mergeVertices } from "three/addons/utils/BufferGeometryUtils.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

// ---------- ruido 3D, para la textura del helado ----------
function crearRuido(semilla = 7) {
  const p = new Uint8Array(512);
  const base = Array.from({ length: 256 }, (_, i) => i);
  let s = semilla;
  for (let i = 255; i > 0; i--) {
    s = (s * 16807) % 2147483647;
    const j = s % (i + 1);
    [base[i], base[j]] = [base[j], base[i]];
  }
  for (let i = 0; i < 512; i++) p[i] = base[i & 255];
  const fade = (t) => t * t * t * (t * (t * 6 - 15) + 10);
  const grad = (h, x, y, z) => {
    const g = h & 15, u = g < 8 ? x : y, v = g < 4 ? y : g === 12 || g === 14 ? x : z;
    return ((g & 1) ? -u : u) + ((g & 2) ? -v : v);
  };
  const lerp = (a, b, t) => a + t * (b - a);
  return (x, y, z) => {
    const X = Math.floor(x) & 255, Y = Math.floor(y) & 255, Z = Math.floor(z) & 255;
    x -= Math.floor(x); y -= Math.floor(y); z -= Math.floor(z);
    const u = fade(x), v = fade(y), w = fade(z);
    const A = p[X] + Y, AA = p[A] + Z, AB = p[A + 1] + Z, B = p[X + 1] + Y, BA = p[B] + Z, BB = p[B + 1] + Z;
    return lerp(
      lerp(lerp(grad(p[AA], x, y, z), grad(p[BA], x - 1, y, z), u), lerp(grad(p[AB], x, y - 1, z), grad(p[BB], x - 1, y - 1, z), u), v),
      lerp(lerp(grad(p[AA + 1], x, y, z - 1), grad(p[BA + 1], x - 1, y, z - 1), u), lerp(grad(p[AB + 1], x, y - 1, z - 1), grad(p[BB + 1], x - 1, y - 1, z - 1), u), v),
      w,
    );
  };
}

// colores tomados de las fotos del producto: fucsia profundo, con luces rosadas y sombras vino
const FUCSIA = new Color("#c80f4b");
const FUCSIA_LUZ = new Color("#ec3a74");
const FUCSIA_SOMBRA = new Color("#6e0326");
const ALTO = 1.3;        // alto del pote
const R_ABAJO = 0.78;    // radio de la base
const R_ARRIBA = 1.0;    // radio de la boca

function radioPote(y) {
  return R_ABAJO + (R_ARRIBA - R_ABAJO) * (y / ALTO);
}

// ---------- etiqueta con el logo y la bajada, como en el pote real ----------
async function texturaLogo(urlLogo) {
  const c = document.createElement("canvas");
  c.width = 2048; c.height = 512;
  const ctx = c.getContext("2d");
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, c.width, c.height);
  try {
    const img = new Image();
    img.decoding = "async";
    img.src = urlLogo;
    await img.decode();
    try { await document.fonts.load("400 40px Bricolage"); } catch { /* sin la fuente, va la del sistema */ }
    const ancho = 520, alto = ancho * (296.795 / 1040);
    // un logo adelante y otro atrás; el de atrás se parte en los dos bordes de la textura
    for (const cx of [c.width * 0.25, c.width * 0.75]) {
      const y = c.height * 0.42 - alto / 2;
      ctx.drawImage(img, cx - ancho / 2, y, ancho, alto);
      ctx.fillStyle = "#3A1320";
      ctx.font = "400 38px Bricolage, sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("Helado tucumano en Salta", cx + 6, y + alto + 40);
    }
  } catch { /* sin logo, el pote queda blanco */ }
  const t = new CanvasTexture(c);
  t.colorSpace = SRGBColorSpace;
  t.anisotropy = 8;
  // la costura de la textura queda a un costado del pote, nunca adelante
  t.offset.x = 0;
  return t;
}

function crearPote(textura) {
  const g = new Group();
  // pared exterior con la etiqueta
  const ext = [];
  for (let i = 0; i <= 24; i++) {
    const y = (i / 24) * ALTO;
    ext.push(new Vector2(radioPote(y), y));
  }
  const exterior = new Mesh(
    new LatheGeometry(ext, 180),
    new MeshPhysicalMaterial({ map: textura, roughness: 0.6, clearcoat: 0.18, clearcoatRoughness: 0.55, envMapIntensity: 0.9 }),
  );
  exterior.rotation.y = -Math.PI / 2; // el logo de adelante mira a la cámara
  g.add(exterior);

  // borde enrollado, interior y base
  const resto = [
    new Vector2(R_ARRIBA, ALTO), new Vector2(R_ARRIBA + 0.028, ALTO + 0.012), new Vector2(R_ARRIBA + 0.036, ALTO + 0.045),
    new Vector2(R_ARRIBA + 0.012, ALTO + 0.07), new Vector2(R_ARRIBA - 0.02, ALTO + 0.058), new Vector2(R_ARRIBA - 0.026, ALTO),
    new Vector2(R_ABAJO - 0.026, 0.06), new Vector2(0.001, 0.06),
  ];
  const papel = new MeshStandardMaterial({ color: "#ffffff", roughness: 0.62, side: DoubleSide });
  g.add(new Mesh(new LatheGeometry(resto, 180), papel));
  const base = new Mesh(new CylinderGeometry(R_ABAJO, R_ABAJO, 0.02, 96), papel);
  base.position.y = 0.01;
  g.add(base);
  return g;
}

// una bocha: esfera densa, deformada con ruido en capas para el raspado y el granulado
function crearBocha(ruido, { detalle, semilla, aplastar = 0.86, base = 0, borde = false }) {
  let geo = new IcosahedronGeometry(1, detalle);
  geo.deleteAttribute("normal");
  geo.deleteAttribute("uv");
  geo = mergeVertices(geo);
  const pos = geo.attributes.position;
  const colores = new Float32Array(pos.count * 3);
  const v = new Vector3();
  const c = new Color();
  const o = semilla * 17.3;
  for (let i = 0; i < pos.count; i++) {
    v.fromBufferAttribute(pos, i);
    const forma = ruido(v.x * 1.3 + o, v.y * 1.3, v.z * 1.3) * 0.12;
    // las capas que deja la cuchara al servir: pliegues marcados en una dirección
    const capa = -Math.abs(ruido(v.x * 1.2 + o, v.y * 6.5 + 4, v.z * 1.2)) * 0.07;
    const pliegue = -Math.abs(ruido(v.x * 2.8 + o, v.y * 2.8 + 4, v.z * 2.8)) * 0.1 + capa;
    const medio = ruido(v.x * 6 + o, v.y * 6, v.z * 6 + 2) * 0.045;
    // granulado: crestas cortas y afiladas, como el hielo raspado
    const g1 = 1 - Math.abs(ruido(v.x * 16 + o, v.y * 16 + 7, v.z * 16));
    const g2 = 1 - Math.abs(ruido(v.x * 38 + o, v.y * 38, v.z * 38 + 3));
    const g3 = ruido(v.x * 80 + o, v.y * 80, v.z * 80);
    const grano = (g1 * g1 - 0.5) * 0.034 + (g2 * g2 * g2 - 0.3) * 0.022 + g3 * 0.006;
    let d = 1 + forma + pliegue + medio + grano;
    let x = v.x * d, y = v.y * d, z = v.z * d;
    // abajo se apoya: se aplana contra el pote o contra las otras bochas
    if (y < base) y = base + (y - base) * 0.25;
    y *= aplastar;
    if (borde) { y = y * 0.32; x *= 1.0; z *= 1.0; }
    pos.setXYZ(i, x, y, z);
    // color: los huecos más oscuros y las crestas más claras, como en la foto
    const hueco = MathUtils.clamp(0.5 + (pliegue + medio) * 6, 0, 1);
    const cresta = MathUtils.clamp((g2 * g2 - 0.4) * 1.8 + g3 * 0.8, 0, 1);
    c.copy(FUCSIA_SOMBRA).lerp(FUCSIA, 0.35 + hueco * 0.65);
    c.lerp(FUCSIA_LUZ, cresta * 0.45);
    colores.set([c.r, c.g, c.b], i * 3);
  }
  geo.setAttribute("color", new BufferAttribute(colores, 3));
  geo.computeVertexNormals();
  return geo;
}

function crearHelado(ruido, movil) {
  const mat = new MeshPhysicalMaterial({
    vertexColors: true, roughness: 0.52, clearcoat: 0.28, clearcoatRoughness: 0.42,
    sheen: 0.18, sheenColor: new Color("#ff5c8f"), sheenRoughness: 0.5, envMapIntensity: 0.45,
  });
  // granulado del hielo raspado: relieve por píxel calculado en la placa de video, así se ve nítido a cualquier tamaño
  mat.onBeforeCompile = (sh) => {
    sh.uniforms.uGrano = { value: 0.04 };
    sh.vertexShader = sh.vertexShader
      .replace("#include <common>", "#include <common>\nvarying vec3 vObj;")
      .replace("#include <begin_vertex>", "#include <begin_vertex>\nvObj = position;");
    sh.fragmentShader = sh.fragmentShader
      .replace("#include <common>", `#include <common>
varying vec3 vObj;
uniform float uGrano;
uniform mat3 normalMatrix;
float hsh(vec3 p) { p = fract(p * 0.3183099 + 0.1); p *= 17.0; return fract(p.x * p.y * p.z * (p.x + p.y + p.z)); }
float vn(vec3 x) {
  vec3 i = floor(x); vec3 f = fract(x); f = f * f * (3.0 - 2.0 * f);
  return mix(mix(mix(hsh(i), hsh(i + vec3(1,0,0)), f.x), mix(hsh(i + vec3(0,1,0)), hsh(i + vec3(1,1,0)), f.x), f.y),
             mix(mix(hsh(i + vec3(0,0,1)), hsh(i + vec3(1,0,1)), f.x), mix(hsh(i + vec3(0,1,1)), hsh(i + vec3(1,1,1)), f.x), f.y), f.z);
}
float granoH(vec3 p) {
  // la octava fina se apaga sola cuando el pote se ve chico, para que no titile
  float fino = 1.0 - smoothstep(0.25, 0.6, length(fwidth(p * 34.0)));
  float h = pow(vn(p * 17.0 + 3.0), 1.3) * 0.6;
  h += (pow(vn(p * 34.0), 1.5) - 0.35) * 0.4 * fino;
  return h + 0.14;
}`)
      .replace("#include <color_fragment>", `#include <color_fragment>
float hGr = granoH(vObj);
diffuseColor.rgb *= mix(0.86, 1.07, hGr);`)
      .replace("#include <normal_fragment_maps>", `#include <normal_fragment_maps>
{
  // pendiente del granulado calculada en el objeto, sin derivadas de pantalla: no se cuadricula
  const float e = 0.004;
  vec3 gO = vec3(granoH(vObj + vec3(e, 0.0, 0.0)), granoH(vObj + vec3(0.0, e, 0.0)), granoH(vObj + vec3(0.0, 0.0, e))) - hGr;
  vec3 gV = normalize(normalMatrix * (gO / e) + 1e-6) * length(gO / e);
  normal = normalize(normal - uGrano * (gV - dot(gV, normal) * normal));
}`);
  };
  mat.customProgramCacheKey = () => "helado-grano";
  const det = movil ? 6 : 7;
  const g = new Group();
  // el colchón que pisa el borde del pote, apenas desbordado
  const colchon = new Mesh(crearBocha(ruido, { detalle: det - 1, semilla: 1, aplastar: 1, borde: true }), mat);
  colchon.scale.set(R_ARRIBA * 1.04, 1, R_ARRIBA * 1.04);
  colchon.position.y = ALTO + 0.06;
  // tres bochas: dos adelante y una arriba, como en el pote de 1 kg
  const bochas = [
    { pos: [-0.36, ALTO + 0.3, 0.26], r: 0.56, s: 2, rot: 0.4 },
    { pos: [0.38, ALTO + 0.28, 0.22], r: 0.55, s: 3, rot: -0.7 },
    { pos: [0.02, ALTO + 0.62, -0.2], r: 0.6, s: 4, rot: 1.9 },
  ];
  g.add(colchon);
  for (const b of bochas) {
    const m = new Mesh(crearBocha(ruido, { detalle: det, semilla: b.s, base: -0.55 }), mat);
    m.scale.setScalar(b.r);
    m.position.set(...b.pos);
    m.rotation.y = b.rot;
    g.add(m);
  }
  return g;
}

/**
 * Monta la escena en un contenedor.
 * opciones: { logo, arrastrable, calidad }
 * Devuelve { estado, renderizar, iniciar, detener, destruir } o null si no hay WebGL.
 */
const pausa = () => new Promise((r) => setTimeout(r, 0));

export async function montarPote(contenedor, opciones = {}) {
  let renderer;
  try {
    renderer = new WebGLRenderer({ antialias: true, alpha: true, powerPreference: "high-performance" });
  } catch {
    return null;
  }
  const movil = matchMedia("(max-width: 700px)").matches;
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, movil ? 1.6 : 2));
  renderer.outputColorSpace = SRGBColorSpace;
  renderer.toneMapping = NeutralToneMapping;
  renderer.toneMappingExposure = 1.0;
  renderer.domElement.setAttribute("aria-hidden", "true");

  await pausa();
  const escena = new Scene();
  const pmrem = new PMREMGenerator(renderer);
  escena.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  escena.environmentIntensity = 0.75;
  pmrem.dispose();

  const camara = new PerspectiveCamera(30, 1, 0.1, 50);
  camara.position.set(0, 1.25, 8.2);
  camara.lookAt(0, 1.05, 0);

  const luz = new DirectionalLight("#fff3e2", 2.15);
  luz.position.set(3.5, 6, 5);
  const relleno = new DirectionalLight("#f3a3b5", 0.9);
  relleno.position.set(-5, 2, 2);
  const contra = new DirectionalLight("#ffffff", 1.4);
  contra.position.set(-1, 4, -5);
  escena.add(luz, relleno, contra, new HemisphereLight("#ffffff", "#e7364a", 0.5));

  await pausa();
  performance.mark("p3d-inicio");
  const ruido = crearRuido();
  const textura = await texturaLogo(opciones.logo);
  performance.mark("p3d-textura");
  const pote = new Group();
  pote.add(crearPote(textura));
  await pausa();
  pote.add(crearHelado(ruido, movil));
  await pausa();
  performance.mark("p3d-geometria");
  pote.position.y = -0.95;
  const pivote = new Group();
  pivote.add(pote);
  escena.add(pivote);

  // estado que manejan las animaciones de scroll
  const estado = { x: 0, y: 0, escala: 1, giroY: -0.35, giroX: 0.12, giroZ: 0, giroAuto: 0.18, visible: 1 };
  const puntero = { x: 0, y: 0, ax: 0, ay: 0 };
  let arrastre = 0, arrastrando = false, ultimoX = 0, inercia = 0;

  let medida = "";
  function medir() {
    const w = contenedor.clientWidth, h = contenedor.clientHeight;
    if (!w || !h || medida === w + "x" + h) return;
    medida = w + "x" + h;
    renderer.setSize(w, h, false);
    camara.aspect = w / h;
    // en pantallas angostas alejamos la cámara para que el pote entre entero
    camara.position.z = w / h < 0.8 ? 11.5 : 8.2;
    camara.updateProjectionMatrix();
  }
  medir();
  contenedor.appendChild(renderer.domElement);
  const ro = new ResizeObserver(medir);
  ro.observe(contenedor);

  const alMover = (e) => {
    puntero.x = (e.clientX / innerWidth) * 2 - 1;
    puntero.y = (e.clientY / innerHeight) * 2 - 1;
  };
  addEventListener("pointermove", alMover, { passive: true });

  if (opciones.arrastrable) {
    const el = renderer.domElement;
    el.style.touchAction = "pan-y";
    el.addEventListener("pointerdown", (e) => { arrastrando = true; ultimoX = e.clientX; el.setPointerCapture(e.pointerId); });
    el.addEventListener("pointermove", (e) => {
      if (!arrastrando) return;
      const dx = e.clientX - ultimoX; ultimoX = e.clientX;
      arrastre += dx * 0.012; inercia = dx * 0.012;
    });
    const soltar = () => { arrastrando = false; };
    el.addEventListener("pointerup", soltar);
    el.addEventListener("pointercancel", soltar);
  }

  let tiempo = 0, ultimo = performance.now(), activo = false, id = 0;
  function renderizar() {
    const ahora = performance.now();
    const dt = Math.min((ahora - ultimo) / 1000, 0.05);
    ultimo = ahora;
    tiempo += dt;
    if (!arrastrando) { arrastre += inercia; inercia *= 0.94; }
    puntero.ax += (puntero.x - puntero.ax) * 0.05;
    puntero.ay += (puntero.y - puntero.ay) * 0.05;
    pivote.position.set(estado.x, estado.y + Math.sin(tiempo * 1.1) * 0.05, 0);
    pivote.scale.setScalar(estado.escala);
    pivote.rotation.set(
      estado.giroX + puntero.ay * 0.12,
      estado.giroY + tiempo * estado.giroAuto + arrastre + puntero.ax * 0.25,
      estado.giroZ + Math.sin(tiempo * 0.8) * 0.02,
    );
    const lienzo = renderer.domElement;
    lienzo.style.opacity = String(estado.visible);
    lienzo.style.visibility = estado.visible > 0.001 ? "visible" : "hidden";
    if (estado.visible > 0.001) renderer.render(escena, camara);
  }
  function bucle() { if (!activo) return; renderizar(); id = requestAnimationFrame(bucle); }
  const iniciar = () => { if (activo) return; activo = true; ultimo = performance.now(); bucle(); };
  const detener = () => { activo = false; cancelAnimationFrame(id); };

  // solo dibuja cuando el contenedor está en pantalla
  const io = new IntersectionObserver(([e]) => (e.isIntersecting ? iniciar() : detener()));
  io.observe(contenedor);
  document.addEventListener("visibilitychange", () => (document.hidden ? detener() : iniciar()));

  // compila los programas gráficos en paralelo para no trabar la página
  await pausa();
  try { await renderer.compileAsync(escena, camara); } catch { /* navegador sin compilación en paralelo */ }
  await pausa();
  performance.mark("p3d-compilado");
  renderizar();
  performance.mark("p3d-primer-cuadro");
  const api = {
    estado, renderizar, iniciar, detener, get activo() { return activo; },
    destruir() { detener(); ro.disconnect(); io.disconnect(); removeEventListener("pointermove", alMover); renderer.dispose(); },
  };
  contenedor.pote = api;
  return api;
}
