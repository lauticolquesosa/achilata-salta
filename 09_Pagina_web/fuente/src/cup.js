// El pote de achilata en 3D. Todo es geometría generada acá: no se descarga ningún modelo.
import {
  WebGLRenderer, Scene, PerspectiveCamera, Group, Mesh, InstancedMesh, Object3D,
  LatheGeometry, SphereGeometry, CapsuleGeometry, OctahedronGeometry, CylinderGeometry,
  MeshPhysicalMaterial, MeshStandardMaterial, CanvasTexture, Vector2, Vector3, Color,
  DirectionalLight, HemisphereLight, PMREMGenerator, SRGBColorSpace, ACESFilmicToneMapping,
  DoubleSide, BufferAttribute, MathUtils,
} from "three";
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

const ROJO_HELADO = new Color("#9e0a2e");
const ROJO_CLARO = new Color("#c9123f");
const ALTO = 1.3;        // alto del pote
const R_ABAJO = 0.74;    // radio de la base
const R_ARRIBA = 1.0;    // radio de la boca

function radioPote(y) {
  return R_ABAJO + (R_ARRIBA - R_ABAJO) * (y / ALTO);
}

// ---------- etiqueta con el logo, dibujada en un canvas ----------
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
    const ancho = 470, alto = ancho * (296.795 / 1040);
    // dos logos, uno de cada lado del pote
    for (const cx of [0, c.width * 0.5, c.width]) {
      ctx.drawImage(img, cx - ancho / 2, c.height * 0.47 - alto / 2, ancho, alto);
    }
  } catch { /* sin logo, el pote queda blanco */ }
  const t = new CanvasTexture(c);
  t.colorSpace = SRGBColorSpace;
  t.anisotropy = 8;
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
    new LatheGeometry(ext, 160),
    new MeshPhysicalMaterial({ map: textura, roughness: 0.55, clearcoat: 0.25, clearcoatRoughness: 0.6 }),
  );
  g.add(exterior);

  // borde enrollado, interior y base
  const resto = [
    new Vector2(R_ARRIBA, ALTO), new Vector2(R_ARRIBA + 0.03, ALTO + 0.015), new Vector2(R_ARRIBA + 0.035, ALTO + 0.05),
    new Vector2(R_ARRIBA + 0.01, ALTO + 0.075), new Vector2(R_ARRIBA - 0.025, ALTO + 0.06), new Vector2(R_ARRIBA - 0.03, ALTO),
    new Vector2(R_ABAJO - 0.03, 0.06), new Vector2(0.001, 0.06),
  ];
  const papel = new MeshStandardMaterial({ color: "#ffffff", roughness: 0.62, side: DoubleSide });
  g.add(new Mesh(new LatheGeometry(resto, 160), papel));
  const base = new Mesh(new CylinderGeometry(R_ABAJO, R_ABAJO, 0.02, 96), papel);
  base.position.y = 0.01;
  g.add(base);
  return g;
}

function crearHelado(ruido, movil) {
  const geo = movil ? new SphereGeometry(1, 150, 96) : new SphereGeometry(1, 210, 132);
  const pos = geo.attributes.position;
  const colores = new Float32Array(pos.count * 3);
  const v = new Vector3();
  const c = new Color();
  const superficie = [];
  for (let i = 0; i < pos.count; i++) {
    v.fromBufferAttribute(pos, i);
    const arriba = MathUtils.smoothstep(v.y, -0.15, 0.35);
    // forma de bocha servida con cuchara: ondas grandes, luego medianas y el granulado del raspado
    const n1 = ruido(v.x * 1.6, v.y * 1.6, v.z * 1.6) * 0.11;
    const n2 = ruido(v.x * 4.2 + 3, v.y * 4.2, v.z * 4.2) * 0.045;
    const n3 = ruido(v.x * 13 + 9, v.y * 13, v.z * 13) * 0.022;
    const n4 = ruido(v.x * 34, v.y * 34 + 5, v.z * 34) * 0.009;
    const pliegue = Math.abs(ruido(v.x * 2.4 + 11, v.y * 2.4, v.z * 2.4)) * -0.07;
    const d = 1 + (n1 + n2 + n3 + n4 + pliegue) * arriba;
    const x = v.x * d * 0.985, z = v.z * d * 0.985;
    const y = (v.y > 0 ? v.y * 0.86 : v.y * 0.4) * d;
    pos.setXYZ(i, x, y, z);
    const claro = MathUtils.clamp(0.5 + n2 * 9 + n3 * 8, 0, 1) * 0.55;
    c.copy(ROJO_HELADO).lerp(ROJO_CLARO, claro);
    colores.set([c.r, c.g, c.b], i * 3);
    if (v.y > 0.12 && i % 5 === 0) superficie.push([x, y, z]);
  }
  geo.setAttribute("color", new BufferAttribute(colores, 3));
  geo.computeVertexNormals();
  const helado = new Mesh(geo, new MeshPhysicalMaterial({
    vertexColors: true, roughness: 0.62, clearcoat: 0.3, clearcoatRoughness: 0.45,
    sheen: 0.2, sheenColor: new Color("#e7364a"), sheenRoughness: 0.7, envMapIntensity: 0.55,
  }));
  helado.position.y = ALTO + 0.02;

  // cristales de hielo sobre la superficie
  const cantidad = movil ? 220 : 450;
  const cristales = new InstancedMesh(
    new OctahedronGeometry(0.016, 0),
    new MeshStandardMaterial({ color: "#b30d36", roughness: 0.3, metalness: 0 }),
    cantidad,
  );
  const o = new Object3D();
  let semilla = 3;
  const azar = () => ((semilla = (semilla * 16807) % 2147483647) / 2147483647);
  for (let i = 0; i < cantidad; i++) {
    const [x, y, z] = superficie[Math.floor(azar() * superficie.length)];
    o.position.set(x * 1.004, y * 1.004 + ALTO + 0.02, z * 1.004);
    o.rotation.set(azar() * 6.3, azar() * 6.3, azar() * 6.3);
    const s = 0.4 + azar() * 0.8;
    o.scale.set(s, s * (0.6 + azar()), s);
    o.updateMatrix();
    cristales.setMatrixAt(i, o.matrix);
  }
  const g = new Group();
  g.add(helado, cristales);
  return g;
}

function crearCuchara() {
  const madera = new MeshStandardMaterial({ color: "#e6c493", roughness: 0.78 });
  const g = new Group();
  const mango = new Mesh(new CapsuleGeometry(0.06, 1.0, 8, 24), madera);
  mango.scale.z = 0.28;
  mango.position.y = 0.62;
  const pala = new Mesh(new SphereGeometry(0.15, 32, 20), madera);
  pala.scale.set(1, 1.45, 0.3);
  g.add(mango, pala);
  g.position.set(0.28, ALTO + 0.62, 0.12);
  g.rotation.set(-0.25, 0.35, -0.42);
  return g;
}

function crearGoteos() {
  const g = new Group();
  const mat = new MeshStandardMaterial({ color: ROJO_HELADO, roughness: 0.28 });
  const inclinacion = Math.atan((R_ARRIBA - R_ABAJO) / ALTO);
  [[1.05, 0.26], [-1.2, 0.36], [2.5, 0.22], [-2.45, 0.3], [0.62, 0.1]].forEach(([ang, largo]) => {
    const d = new Group();
    const chorro = new Mesh(new CapsuleGeometry(0.045, largo, 8, 20), mat);
    chorro.position.y = -largo / 2;
    chorro.scale.z = 0.7;
    const gota = new Mesh(new SphereGeometry(0.068, 24, 16), mat);
    gota.position.y = -largo - 0.02;
    gota.scale.set(1, 1.2, 0.8);
    d.add(chorro, gota);
    const yTop = ALTO + 0.04;
    d.position.set(Math.sin(ang) * (R_ARRIBA + 0.03), yTop, Math.cos(ang) * (R_ARRIBA + 0.03));
    d.rotation.y = ang;
    d.rotateX(inclinacion);
    g.add(d);
  });
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
  renderer.toneMapping = ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
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

  const luz = new DirectionalLight("#fff3e2", 2.4);
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
  pote.add(crearCuchara(), crearGoteos());
  performance.mark("p3d-geometria");
  pote.position.y = -0.95;
  const pivote = new Group();
  pivote.add(pote);
  escena.add(pivote);

  // estado que manejan las animaciones de scroll
  const estado = { x: 0, y: 0, escala: 1, giroY: -0.35, giroX: 0.12, giroZ: 0, giroAuto: 0.18, visible: 1 };
  const puntero = { x: 0, y: 0, ax: 0, ay: 0 };
  let arrastre = 0, arrastrando = false, ultimoX = 0, inercia = 0;

  function medir() {
    const w = contenedor.clientWidth, h = contenedor.clientHeight;
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
