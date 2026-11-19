# Genera el cronograma de dos semanas: el .md, una carpeta con brief por pieza y por día, y el PDF.
# Uso: python generar.py   (desde cualquier carpeta)
import datetime as dt, os, sys, html, asyncio, pathlib, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datos import INICIO, N_DIAS, PIEZAS, DIAS, COMO_FUNCIONA

BASE = pathlib.Path(__file__).resolve().parents[2]          # 04_Contenido
PROY = BASE.parent
CRON = BASE / "Cronograma"
DC = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
DL = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
MES = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
d0 = dt.date(*INICIO)
F = {i: d0 + dt.timedelta(days=i - 1) for i in range(1, N_DIAS + 1)}
dia_de = {c: i for i, v in DIAS.items() for _, c in v[2]}
hora_de = {c: h for i, v in DIAS.items() for h, c in v[2]}

def larga(d): return f"{DL[d.weekday()]} {d.day} de {MES[d.month]}"
def corta(d): return f"{DC[d.weekday()]} {d.day} {MES[d.month][:3]}"
def carpeta_pieza(c): return BASE / ("Reels" if PIEZAS[c][1] == "Reel" else "Publicaciones") / f"{c} {PIEZAS[c][0]}"
def carpeta_dia(i): return BASE / "Historias" / f"Día {i:02d} {corta(F[i])}"

# ---------- archivo de lo que quedó fuera de las dos semanas ----------
ARCH = BASE / "_archivo cronograma 30 días"
validas = {carpeta_pieza(c).name for c in PIEZAS} | {carpeta_dia(i).name for i in DIAS}
for sub in ["Publicaciones", "Reels", "Historias"]:
    for p in (BASE / sub).iterdir():
        if p.is_dir() and p.name not in validas:
            dest = ARCH / sub / p.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists(): shutil.move(str(p), str(dest))
for viejo in ["cronograma_30_dias.md", "Cronograma Achilata 30 días.pdf"]:
    if (CRON / viejo).exists():
        ARCH.mkdir(exist_ok=True); shutil.move(str(CRON / viejo), str(ARCH / viejo))
for viejo in ["detalle.py"]:
    if (CRON / "fuente" / viejo).exists():
        ARCH.mkdir(exist_ok=True); shutil.move(str(CRON / "fuente" / viejo), str(ARCH / viejo))

# ---------- briefs ----------
ESTADO = ["## Estado", "- [ ] Fotos elegidas de toda la galería, en el momento de hacerla",
          "- [ ] Fotos estudiadas, editadas y adaptadas al formato", "- [ ] Diseño siguiendo el manual",
          "- [ ] Revisado con `04_Contenido/reglas_de_contenido.md`", "- [ ] Enviado al WhatsApp de Lauti, imágenes y texto",
          "- [ ] Publicado y anotado en `registro_publicaciones.md`", ""]
for c, (t, tipo, formato, desc, texto) in PIEZAS.items():
    i = dia_de[c]; d = F[i]
    car = carpeta_pieza(c); car.mkdir(parents=True, exist_ok=True)
    s = [f"# {c} · {t}", "", f"- **Tipo:** {tipo}, {formato.lower()}",
         f"- **Cuándo:** día {i}, {larga(d).lower()}, a las {hora_de[c]} hs",
         f"- **Medida:** {'1080 × 1920 px' if tipo == 'Reel' else '1080 × 1350 px por placa'}", "",
         "## La idea", desc, "", "La idea es una propuesta. Las fotos se eligen recién cuando se pide la pieza, mirando toda la galería.", "",
         "## Texto de la publicación", texto, ""] + ESTADO
    (car / "brief.md").write_text("\n".join(s), encoding="utf-8")
for i, (tema, obj, feed, hist, nota) in DIAS.items():
    car = carpeta_dia(i); car.mkdir(parents=True, exist_ok=True)
    s = [f"# Historias del día {i} · {larga(F[i])}", "", f"**Tema:** {tema}. {obj}", ""]
    s += [f"{k}. **{h} hs.** {x}" for k, (h, x) in enumerate(hist, 1)]
    s += ["", "Medida 1080 × 1920 px, con 250 px libres arriba y abajo.", ""] + ESTADO
    (car / "brief.md").write_text("\n".join(s), encoding="utf-8")

def indice(nombre, codes):
    s = [f"# {nombre}", "", "| Código | Día | Hora | Pieza | Formato |", "|---|---|---|---|---|"]
    for c in codes:
        s.append(f"| {c} | {corta(F[dia_de[c]])} | {hora_de[c]} | {PIEZAS[c][0]} | {PIEZAS[c][2]} |")
    return "\n".join(s) + "\n"
orden = sorted(PIEZAS, key=lambda c: (dia_de[c], hora_de[c]))
(BASE / "Publicaciones" / "_indice.md").write_text(indice("Publicaciones", [c for c in orden if PIEZAS[c][1] != "Reel"]), encoding="utf-8")
(BASE / "Reels" / "_indice.md").write_text(indice("Reels", [c for c in orden if PIEZAS[c][1] == "Reel"]), encoding="utf-8")
total_h = sum(len(v[3]) for v in DIAS.values())
(BASE / "Historias" / "_indice.md").write_text(f"# Historias\n\nUna carpeta por día con su brief. Son {total_h} historias en {N_DIAS} días.\n", encoding="utf-8")

# ---------- .md ----------
n_pub = sum(1 for c in PIEZAS if PIEZAS[c][1] != "Reel"); n_reel = len(PIEZAS) - n_pub
md = ["# Cronograma de dos semanas · @achilatasalta", "",
      f"Del {larga(F[1]).lower()} al {larga(F[N_DIAS]).lower()} de 2026: {n_pub} publicaciones, {n_reel} reels y {total_h} historias.",
      "Se sube algo todos los días, y más de jueves a domingo.", "",
      "Lo generan `Cronograma/fuente/datos.py` y `generar.py`.", "", "## Cómo funciona", ""]
for t, x in COMO_FUNCIONA: md += [f"**{t}.** {x}", ""]
for i, (tema, obj, feed, hist, nota) in DIAS.items():
    md += [f"## Día {i} · {larga(F[i])} · {tema}", "", obj, ""]
    for h, c in feed:
        t, tipo, formato, desc, texto = PIEZAS[c]
        md += [f"**{h} hs · {tipo} {c} · {t}** · {formato}", "", desc, "", f"*Texto:* {texto}", ""]
    md += ["**Historias**", ""] + [f"- {h} hs. {x}" for h, x in hist] + [""]
    if nota: md += [f"> {nota}", ""]
(CRON / "cronograma_2_semanas.md").write_text("\n".join(md), encoding="utf-8")

# ---------- PDF ----------
def u(p): return pathlib.Path(p).resolve().as_uri()
FONTS = pathlib.Path(os.environ["LOCALAPPDATA"]) / "Microsoft/Windows/Fonts"
LOGO = u(PROY / "06_Assets/logo/achilata-sin-bajada-rojo.png")
e = html.escape

lunes = F[1] - dt.timedelta(days=F[1].weekday())
idx = {v: k for k, v in F.items()}
celdas, cur = [], lunes
while cur <= F[N_DIAS] or cur.weekday() != 0:
    i = idx.get(cur)
    if not i:
        celdas.append(f'<div class="cel fuera"><span class="num">{cur.day}</span></div>')
    else:
        tema, obj, feed, hist, nota = DIAS[i]
        items = "".join(f'<div class="it {"r" if PIEZAS[c][1]=="Reel" else "p"}"><i></i>{e(PIEZAS[c][0])}</div>' for _, c in feed)
        items += f'<div class="it h"><i></i>{len(hist)} historias</div>'
        cls = "cel" + (" finde" if cur.weekday() >= 3 else "") + (" uno" if i == 1 else "")
        celdas.append(f'<div class="{cls}"><span class="num">{cur.day}</span><span class="dd">día {i}</span>{items}</div>')
    cur += dt.timedelta(days=1)

texto = ['<section class="txt"><p class="sub">Antes de empezar</p><h2><i></i>Cómo funciona el cronograma</h2>']
for t, x in COMO_FUNCIONA: texto.append(f'<h4>{e(t)}</h4><p>{e(x)}</p>')
texto.append("</section>")
for i, (tema, obj, feed, hist, nota) in DIAS.items():
    sem = 1 if i <= 4 else (2 if i <= 11 else 3)
    b = [f'<section class="txt"><p class="sub">Semana {sem} · {larga(F[i])} · Día {i}</p><h2><i></i>{e(tema)}</h2><p>{e(obj)}</p>']
    for h, c in feed:
        t, tipo, formato, desc, tx = PIEZAS[c]
        b.append(f'<h4>{h} hs · {tipo} · {e(t)}</h4><p class="meta">{e(formato)}</p><p>{e(desc)}</p><p class="cap">Texto para publicar: {e(tx)}</p>')
    b.append('<h4>Historias</h4>' + "".join(f'<p class="hi"><span>{h}</span>{e(x)}</p>' for h, x in hist))
    if nota: b.append(f'<p class="nota">{e(nota)}</p>')
    b.append("</section>")
    texto.append("".join(b))

css = f"""
@font-face{{font-family:BX;src:url('{u(FONTS/"BricolageGrotesque-ExtraBold.ttf")}')}}
@font-face{{font-family:BR;src:url('{u(FONTS/"BricolageGrotesque-Regular.ttf")}')}}
@page{{size:A4;margin:20mm 20mm 20mm 20mm}}
@page:first{{margin:0}}
:root{{--rojo:#E7364A;--rosa:#F3A3B5;--crema:#FFF3E2;--bordo:#3A1320}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{font-family:BR,Arial,sans-serif;color:#000;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.tapa{{width:210mm;height:297mm;padding:18mm 16mm;background:var(--crema);color:var(--bordo);page-break-after:always;position:relative}}
.tapa h1{{font-family:BX;font-weight:400;font-size:34pt;line-height:.95;color:var(--rojo)}}
.tapa .s{{font-size:10pt;margin-top:3mm;line-height:1.45}}
.tapa .logo{{position:absolute;right:16mm;top:20mm;height:10mm}}
.cal{{display:grid;grid-template-columns:repeat(7,1fr);gap:1.8mm;margin-top:11mm}}
.cab{{font-family:BX;font-size:8pt;color:var(--rojo);letter-spacing:.06em;padding-bottom:1mm}}
.cel{{background:#fff;border-radius:2.5mm;padding:2.4mm;height:48mm;position:relative;overflow:hidden}}
.cel.finde{{background:#FCE3E8}}
.cel.uno{{background:var(--rojo);color:var(--crema)}} .cel.uno .it i{{background:var(--crema)!important}}
.cel.fuera{{background:transparent;border:.3mm solid #EAD9CB}} .cel.fuera .num{{color:#D9C6B8}}
.num{{font-family:BX;font-size:15pt;line-height:1}}
.dd{{position:absolute;right:2.4mm;top:2.8mm;font-size:6.5pt;opacity:.7}}
.it{{font-size:7.2pt;line-height:1.25;margin-top:1.6mm;display:flex;gap:1.3mm;align-items:baseline}}
.it i{{width:1.8mm;height:1.8mm;border-radius:50%;flex:none}}
.it.p i{{background:var(--rojo)}} .it.r i{{background:var(--bordo)}} .it.h i{{background:var(--rosa)}}
.ley{{display:flex;flex-wrap:wrap;gap:3mm 7mm;font-size:8pt;margin-top:6mm}}
.ley span{{display:flex;gap:1.6mm;align-items:center}}
.ley i{{width:2.4mm;height:2.4mm;border-radius:50%;display:inline-block}}
.ley b{{width:4.5mm;height:3.2mm;border-radius:.8mm;display:inline-block;font-weight:400}}
.res{{margin-top:9mm;font-size:9.5pt;line-height:1.55;max-width:150mm}}
.txt{{margin-bottom:11mm;break-inside:auto}}
.txt .sub{{font-size:8.5pt;color:var(--rojo);letter-spacing:.04em;margin-bottom:1.5mm}}
.txt h2{{font-family:BX;font-weight:400;font-size:19pt;line-height:1.1;color:var(--bordo);margin-bottom:3mm;display:flex;align-items:center;gap:3mm;break-after:avoid}}
.txt h2 i{{width:3.2mm;height:3.2mm;border-radius:50%;background:var(--rojo);flex:none}}
.txt h4{{font-family:BX;font-weight:400;font-size:10.5pt;color:var(--bordo);margin:5mm 0 1.5mm;break-after:avoid}}
.txt p{{font-size:10pt;line-height:1.6;margin-bottom:2mm;text-align:left}}
.txt .meta{{font-size:8.5pt;color:#555;margin-bottom:1.2mm}}
.txt .cap{{margin-top:1mm}}
.txt .hi{{display:flex;gap:4mm;margin-bottom:1.2mm}}
.txt .hi span{{width:11mm;flex:none;color:var(--rojo)}}
.txt .nota{{margin-top:3mm;padding-left:4mm;border-left:.6mm solid var(--rosa)}}
"""

doc = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="tapa"><img class="logo" src="{LOGO}">
 <h1>Cronograma<br>de dos semanas</h1>
 <p class="s">Del {larga(F[1]).lower()} al {larga(F[N_DIAS]).lower()} de 2026<br>{n_pub} publicaciones · {n_reel} reels · {total_h} historias</p>
 <div class="cal">{''.join(f'<div class="cab">{x.upper()}</div>' for x in DC)}{''.join(celdas)}</div>
 <div class="ley"><span><i style="background:var(--rojo)"></i>Publicación</span><span><i style="background:var(--bordo)"></i>Reel</span><span><i style="background:var(--rosa)"></i>Historias</span><span><b style="background:#FCE3E8"></b>Jueves a domingo, días de venta</span></div>
 <p class="res">Se sube algo todos los días. De lunes a miércoles, una publicación a las 20 hs y pocas historias. De jueves a domingo, una o dos publicaciones, a las 13 y a las 20 hs, y entre cinco y siete historias. Es una base: cualquier día se pueden pedir piezas nuevas y el cronograma se acomoda.</p>
</div>
{''.join(texto)}
</body></html>"""

src = CRON / "fuente" / "cronograma.html"
src.write_text(doc, encoding="utf-8")
SALIDA = CRON / "Cronograma Achilata 2 semanas.pdf"
async def pdf():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto(src.as_uri()); await pg.wait_for_timeout(800)
        await pg.pdf(path=str(SALIDA), format="A4", print_background=True, prefer_css_page_size=True)
        await b.close()
asyncio.run(pdf())
print("ok", n_pub, n_reel, total_h)
