# Perfil completo · 26/11/2026

Pedido de Lauti: llenar el feed, armar las destacadas y las próximas historias, con el modelo de Rocambolesc, títulos en crema y fondo rojo achilata. **Este plan manda sobre el cronograma de 2 semanas, que queda en pausa.**

- `Perfil completo Achilata.pdf`: la guía de qué subir, en qué orden y qué cambiar. Sale de `fuente/generar_pdf.py`.
- `textos_para_copiar.md`: la presentación y los textos de las 10 publicaciones, con emojis.
- `maqueta del perfil.png`: cómo queda la grilla de 12.
- `foto de perfil 1080.png`: el logo rojo sobre blanco, más grande.

## Orden de publicación
1. P03 Achilata, sustantivo · 2. P04 La textura · 3. P05 Hace 32 grados · 4. P06 Cómo pedir · 5. P07 Una cucharada · 6. P08 Etiquetá · 7. P09 No deslices · 8. P10 La achilata anotada · 9. P11 Te la llevamos · 10. P12 Achilata en tu fiesta.

## Dónde está cada cosa
- Las 12 del feed, reels incluidos: `04_Contenido/Publicaciones/P01` a `P12`, numeradas en el orden en que se suben, cada una con su `final/`.
- Destacadas: `04_Contenido/Destacadas`, portadas y historias.
- Próximas historias: `04_Contenido/Historias/Próximas historias`.
- Scripts: `06_Assets/fotos/herramientas/feed_comun.py`, `build_feed_posts.py`, `build_feed_reels.py`, `build_feed_historias.py` y `build_perfil_maqueta.py`. Necesitan la carpeta de recortes `a??.npy` y `f??.npy` como primer argumento.
