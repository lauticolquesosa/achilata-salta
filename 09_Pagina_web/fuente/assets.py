"""Prepara las imágenes, las fuentes, los logos y los íconos de la web.

Uso, desde 09_Pagina_web/fuente:
    python assets.py

Lee de 06_Assets y escribe en ../sitio/assets. Se corre solo cuando cambian
las fotos o los logos. Las fotos salen en AVIF y WebP, en dos anchos.
"""

import json
import pathlib
import re

from fontTools import subset
from PIL import Image, ImageDraw

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
FOTOS = RAIZ / "06_Assets" / "fotos"
SITIO = AQUI.parent / "sitio"
IMG = SITIO / "assets" / "img"
FUENTES = SITIO / "assets" / "fonts"

# nombre en la web: archivo original. Solo fotos aprobadas, sin textos de otras marcas.
O = "originales 19-11/"
E = "editadas/estudio rojo/"
FOTOS_WEB = {
    "palmera-mano": O + "01 Copa de sorbete fucsia Achilata (1).png",
    "cuchara-amarillo": O + "02 Copa de sorbete fucsia Achilata.png",
    "mano-bordo": O + "05 Gelato fucsia en vaso Achilata.png",
    "sol-cuchara-madera": O + "06 Gelato rosado al sol.png",
    "cuchara-negro": O + "07 Helado achilata de sorbetes rojos.png",
    "pote-gris": O + "08 Helado fucsia derritiéndose en vaso blanco.png",
    "bocha-cuchara": O + "10 Helado fucsia en cuchara metálica.png",
    "pote-grande": O + "11 Helado fucsia en vaso Achilata.png",
    "mano-cuchara-bordo": O + "12 Helado fucsia en vaso blanco.png",
    "cielo": O + "14 Helado tucumano bajo el cielo azul.png",
    "pila-potes": O + "15 Pila de helados Achilata.png",
    "pote-cuchara": O + "16 Primer plano de gelato fucsia Achilata.png",
    "remera-cuchara": O + "20 Sorbete fucsia con logo achilata.png",
    "cuchara-madera-cielo": O + "21 Sorbete fucsia en cuchara de madera.png",
    "bochas": O + "22 Sorbete fucsia en vaso blanco.png",
    "pasto": O + "23 Sorbete magenta en vaso achilata.png",
    "oliva": O + "24 Sorbete rojo en vaso blanco.png",
    "fila-tres": O + "27 Vasitos de sorbete rojo intenso.png",
    "pote-oscuro": O + "28 Vaso de achilata fucsia.png",
    "oliva-servilleta": O + "29 Vaso de achilata sobre fondo verde oliva.png",
    "bordo-mano": O + "31 Vaso de achilata tucumana con logo rojo.png",
    "fila-potes": O + "32 Vasos de achilata tucumana en fila.png",
    "textura": "editadas/copa-primer-plano-4x5.png",
    "rojo-cuchara": E + "02 estudio rojo.png",
    "rojo-mano": E + "05 estudio rojo.png",
    "rojo-negro": E + "07 estudio rojo.png",
    "rojo-bocha": E + "10 estudio rojo.png",
    "rojo-mano-cuchara": E + "11 estudio rojo.png",
    "rojo-scoop": E + "13 estudio rojo.png",
    "rojo-pote": E + "16 estudio rojo.png",
}
ANCHOS = (640, 1100)


def fotos():
    IMG.mkdir(parents=True, exist_ok=True)
    medidas = {}
    for nombre, rel in FOTOS_WEB.items():
        im = Image.open(FOTOS / rel).convert("RGB")
        medidas[nombre] = {"w": im.width, "h": im.height}
        for ancho in ANCHOS:
            a = min(ancho, im.width)
            r = im.resize((a, round(im.height * a / im.width)), Image.LANCZOS)
            r.save(IMG / f"{nombre}-{ancho}.avif", quality=58, speed=4)
            r.save(IMG / f"{nombre}-{ancho}.webp", quality=80, method=6)
    (AQUI / "src" / "medidas.json").write_text(json.dumps(medidas, indent=1), encoding="utf-8")
    print("fotos", len(FOTOS_WEB))


def fuentes():
    FUENTES.mkdir(parents=True, exist_ok=True)
    texto = (" !#$%&*+,./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]_abcdefghijklmnopqrstuvwxyz"
             "ÁÉÍÓÚÜÑáéíóúüñ¿¡·×°ºª€©®→←↑↓−")
    for peso in ("Regular", "ExtraBold"):
        o = subset.Options()
        o.flavor = "woff2"
        o.layout_features = ["kern", "liga", "calt"]
        o.name_IDs = ["*"]  # conserva la licencia OFL dentro del archivo
        f = subset.load_font(str(RAIZ / "06_Assets" / "fuentes" / f"BricolageGrotesque-{peso}.ttf"), o)
        s = subset.Subsetter(o)
        s.populate(text=texto)
        s.subset(f)
        subset.save_font(f, str(FUENTES / f"bricolage-{peso.lower()}.woff2"), o)
    print("fuentes ok")


def logos():
    """Deja los SVG limpios: sin estilos incrustados, para que la CSP estricta los acepte."""
    destino = SITIO / "assets" / "img"
    for color in ("rojo", "blanco", "crema", "bordo"):
        t = (RAIZ / "06_Assets" / "logo" / f"achilata-sin-bajada-{color}.svg").read_text(encoding="latin-1")
        t = re.sub(r"<\?xml.*?\?>|<!--.*?-->", "", t, flags=re.S)
        t = re.sub(r'style="fill:(#[0-9A-Fa-f]{6});?"', r'fill="\1"', t)
        t = re.sub(r'\s(style|id|x|y|xml:space|enable-background|version)="[^"]*"', "", t)
        t = t.replace('xmlns:xlink="http://www.w3.org/1999/xlink"', "")
        t = re.sub(r">\s+<", "><", t).strip()
        t = t.replace("<svg ", '<svg role="img" aria-label="achilata." width="1040" height="297" ', 1)
        assert "style" not in t and "<script" not in t
        (destino / f"logo-{color}.svg").write_text(t, encoding="utf-8")
    print("logos ok")


def iconos():
    """Ícono de la pestaña: el logo entero en blanco sobre rojo, nunca la reducida."""
    import io
    import subprocess
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    svg = (SITIO / "assets" / "img" / "logo-blanco.svg").read_text(encoding="utf-8")

    def render(w, h, logo_w, nombre, foto=None):
        html = SITIO.parent / "fuente" / "_tmp_icono.html"
        fondo = "#E7364A"
        img_foto = ""
        if foto:
            img_foto = f'<img src="{foto.as_uri()}" style="position:absolute;right:0;top:0;height:100%">'
        html.write_text(
            f'<html><body style="margin:0;width:{w}px;height:{h}px;background:{fondo};position:relative;overflow:hidden">'
            f'{img_foto}<div style="position:absolute;left:{(w - logo_w) // 2 if not foto else 80}px;'
            f'top:{h // 2 - logo_w * 0.1425}px;width:{logo_w}px">{svg}</div></body></html>', encoding="utf-8")
        png = SITIO / nombre
        subprocess.run([chrome, "--headless=new", "--allow-file-access-from-files", "--hide-scrollbars",
                        f"--window-size={w},{h}", f"--screenshot={png}", html.as_uri()],
                       check=True, capture_output=True)
        html.unlink()
        return png

    render(512, 512, 430, "icon-512.png")
    render(192, 192, 166, "icon-192.png")
    render(180, 180, 156, "apple-touch-icon.png")
    p = render(48, 48, 44, "_fav48.png")
    Image.open(p).save(SITIO / "favicon.ico", sizes=[(48, 48), (32, 32), (16, 16)])
    p.unlink()
    foto = FOTOS / E / "16 estudio rojo.png"
    og = render(1200, 630, 560, "_og.png", foto)
    Image.open(og).convert("RGB").save(IMG / "compartir.jpg", quality=86)
    og.unlink()
    print("iconos ok")


if __name__ == "__main__":
    fotos()
    fuentes()
    logos()
    iconos()
