# Perfil completo · 26/11/2026

Pedido de Lauti: llenar el feed, armar las destacadas y las próximas historias, con el modelo de Rocambolesc, títulos en crema y fondo rojo achilata. **Este plan manda sobre el cronograma de 2 semanas, que queda en pausa.**

- `Perfil completo Achilata.pdf`: la guía de qué subir, en qué orden y qué cambiar. Sale de `fuente/generar_pdf.py`.
- `textos_para_copiar.md`: la presentación y los textos de las 10 publicaciones, con emojis.
- `maqueta del perfil.png`: cómo queda la grilla de 12.
- `foto de perfil 1080.png`: el logo rojo sobre blanco, más grande.

## Orden de publicación
1. P08 Achilata, sustantivo · 2. R03 La textura · 3. P04 Hace 32 grados · 4. P09 Cómo pedir · 5. R01 Una cucharada · 6. P11 Etiquetá · 7. P05 No deslices · 8. P10 La achilata anotada · 9. R07 Te la llevamos · 10. P13 Achilata en tu fiesta.

## Dónde está cada cosa
- Publicaciones y reels: su carpeta en `04_Contenido/Publicaciones` y `Reels`, en `final/`.
- Destacadas: `04_Contenido/Destacadas`, portadas y historias.
- Próximas historias: `04_Contenido/Historias/Próximas historias`.
- Scripts: `06_Assets/fotos/herramientas/feed_comun.py`, `build_feed_posts.py`, `build_feed_reels.py`, `build_feed_historias.py` y `build_perfil_maqueta.py`. Necesitan la carpeta de recortes `a??.npy` y `f??.npy` como primer argumento.
