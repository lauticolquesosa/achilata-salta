# Perfil completo · 26/11/2026

Pedido de Lauti: llenar el feed, armar las destacadas y las próximas historias, con el modelo de Rocambolesc, títulos en crema y fondo rojo achilata. El cronograma quedó congelado el 26/11 y las publicaciones no tienen fecha: se marcan como subidas o no subidas.

- `Perfil completo Achilata.pdf`: la guía de qué subir, en qué orden y qué cambiar. Sale de `fuente/generar_pdf.py`.
- `textos_para_copiar.md`: la presentación y los textos de las 10 publicaciones, con emojis.
- `maqueta del perfil.png`: cómo queda la grilla de 12.
- `foto de perfil 1080.png`: el logo rojo sobre blanco, más grande.

## Orden de publicación
El de `04_Contenido/Publicaciones/_indice.md`: P01 a P12, el número es el lugar en la grilla.

## Dónde está cada cosa
- Las 12 del feed, reels incluidos: `04_Contenido/Publicaciones/P01` a `P12`, numeradas en el orden en que se suben, cada una con su `final/`.
- Destacadas: `04_Contenido/Destacadas`, portadas y historias.
- Historias: `04_Contenido/Historias`, de H01 en adelante, con `_indice.md`. Las próximas historias interactivas son H18 a H23.
- Scripts: `06_Assets/fotos/herramientas/feed_comun.py`, `build_feed_posts.py`, `build_feed_reels.py`, `build_feed_historias.py` y `build_perfil_maqueta.py`. Necesitan la carpeta de recortes `a??.npy` y `f??.npy` como primer argumento.
