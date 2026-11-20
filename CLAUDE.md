# Achilata Salta · Reglas del proyecto

Este proyecto existe para crear el contenido de **@achilatasalta**: publicaciones, historias, reels y piezas para Instagram y TikTok.

Es un emprendimiento de Lauti y un amigo que vende **achilata**, el helado de agua tucumano, en **Salta Capital** durante la temporada de verano 2026-2027. El producto lo resuelve un proveedor. El trabajo de este proyecto es la marca y las redes.

## Antes de crear cualquier pieza, leer en este orden

1. `02_Marca/Manual de marca/Exportes/Paginas/`: las 33 páginas del manual. **Es la ley.** La fuente editable es `02_Marca/Manual de marca/Achilata Manual de Marca.ai`.
2. `04_Contenido/reglas_de_contenido.md`: el checklist que tiene que pasar cada pieza.
3. `03_Estrategia/sistema_de_contenido.md`: las 11 series fijas, el ritmo de la grilla, las historias y la interacción. Sale de `05_Referencias/analisis_de_referencias.md`, el análisis de casi 30 cuentas de heladerías y marcas de comida de Estados Unidos, Europa, Australia y Argentina. La más cercana a nosotros es Kuono y de los carruseles de LCS Publicidad.
4. **Datos confirmados para publicar:**
   - 1 kg a $12.000 y medio kilo a $8.000.
   - WhatsApp 387 483 4041 y 387 468 4498. Van los dos.
   - Delivery en Grand Bourg, San Lorenzo Chico, San Lorenzo, El Tipal y La Almudena. Las otras zonas se consultan.
   - Pago por transferencia o en efectivo.
   - Solo el sabor clásico.
   - Solo potes de 1 kg y medio kilo. **No hay vasitos:** en el feed pueden aparecer como referencia estética, pero nunca se ofrecen como producto ni con precio.

## Cronograma y piezas
- **El cronograma es de dos semanas,** del jueves 19/11 al miércoles 2/12/2026. Está en `04_Contenido/Cronograma/`:
  - `cronograma_2_semanas.md`;
  - el PDF, `Cronograma Achilata 2 semanas.pdf`;
  - y su `fuente/`. **Todo sale de `fuente/datos.py`:** si se cambia algo, se edita ahí y se corre `python generar.py`, que rehace el `.md`, las carpetas y el PDF.
  - El cronograma viejo de 30 días está en `04_Contenido/_archivo cronograma 30 días/`.
- **Se sube algo todos los días,** y más de jueves a domingo. **El cronograma es una base, no algo fijo:**
  - Si Lauti pide una pieza que no estaba, como una historia con los precios para hoy, se hace en el momento.
  - Después se acomoda `datos.py`: si la pieza nueva reemplaza algo previsto, eso se saca o se mueve a otro día; si suma, lo demás queda igual.
- **Cada pieza se hace recién cuando Lauti la pide, nunca por adelantado:**
  1. Revisar **toda** la galería, `06_Assets/fotos/` y lo nuevo en Descargas, y elegir la mejor foto para esa pieza.
  2. Estudiarla al 100 %, editarla y adaptarla al formato, según la sección 1b de `reglas_de_contenido.md`.
  3. Diseñarla siguiendo el manual.
  4. Guardarla en su carpeta, en `final/`.
- **Al terminar una pieza:**
  1. Mandar al chat yo de WhatsApp todas las imágenes **como documento y en orden**.
  2. Después, en un mensaje aparte, mandar **solo el texto limpio** para copiar en Instagram.
  3. Anotarla en `registro_publicaciones.md`.
- **La presentación del perfil** está en `03_Estrategia/perfil_instagram.md`.
- **Cada pieza tiene su carpeta con un `brief.md`:**
  - `04_Contenido/Publicaciones/P01…P19`
  - `Reels/R01…R13`
  - `Historias/Día 01…30`
- **Lo terminado** de cada pieza se guarda en su carpeta, con su PNG o MP4 final.
- **La publicación vieja ya está archivada.** P01 es la primera desde la vuelta. La cuenta tenía 542 seguidores.
- **Posicionamiento:** más rica y cuidada que la achilata de barrio, más barata que una heladería artesanal. Nunca se compite por precio. Ver `01_Contexto/03_mercado_salta.md`.

Por ahora el trabajo es **solo Instagram**. La cuenta arranca con 0 publicaciones.
5. `01_Contexto/`: el negocio, el producto, Salta, el público y la competencia.
6. `05_Referencias/`: las cuentas y las imágenes de referencia, con lo que se toma de cada una.
7. `07_Pendientes.md`: lo que todavía no está confirmado. Lo no confirmado no se publica como dato.
8. `08_Eventos/`: el servicio de carrito de achilata para eventos, sumado el 19/11/2026. Para cualquier pieza, precio o contacto de eventos, leer primero `08_Eventos/00_LEEME.md`. **Los vasitos existen solo en eventos;** la venta a domicilio sigue siendo solo potes.
9. `09_Pagina_web/`: la web de la marca, publicada en https://achilata-salta.vercel.app. Se edita en `fuente/` y se genera con `node build.mjs`; los precios salen de `fuente/src/datos.json`. Leer su `LEEME.md` antes de tocarla. Mantiene las mismas reglas de texto: sin comillas, guiones ni paréntesis.

## La marca, en corto

- **Logo:** `achilata.` en minúscula, Bricolage Grotesque ExtraBold, con goteo en las dos a y punto final. Bajada: *Helado tucumano en Salta*. Hay 3 versiones: principal, sin bajada y reducida (la `a.`). **Foto de perfil: logo principal rojo sobre blanco.** `02_Marca/Logo/logo.ai` tiene todas las combinaciones aprobadas, una por mesa, con su PNG de 1080 px en `PNG 1080/`. También hay exportes en `06_Assets/logo/`.
- **Colores:**
  - Predominantes: rojo **#E7364A** y crema **#FFF3E2**.
  - Detalles: rosa **#F3A3B5**, blanco **#FFFFFF** y bordó **#3A1320**.
  - Cuando sea necesario: negro **#000000**.
- **Tipografías:**
  - Bricolage Grotesque **ExtraBold** para títulos.
  - Bricolage Grotesque **Regular** para textos.
  - **Ink Free** solo para detalles y resaltados.
- **Tramas:** solo en ocasiones especiales, como máximo una cada nueve publicaciones.
- **Goteo para contenido:** son los fondos de goteo rojo sobre gofre bordó o rosa, en `02_Marca/Manual de marca/Links/`. El texto va siempre en la zona del gofre.

## Correcciones de Lauti del 19/11/2026 · mandan sobre el manual
- **El bordó, solo en detalles mínimos.** Nunca va de fondo ni en bloques.
- **Los fondos son rojo achilata con el texto en blanco.** El crema puede ir de fondo a veces.
- **Los títulos en ExtraBold llevan un borde del mismo color,** para que queden más anchos y pesados.
- **Fotos en casi todas las placas de un carrusel,** y todas con la misma estética. Pocos fondos lisos.
- **El logo, siempre entero y sin bajada.** Nunca la reducida `a.`.
- **La foto y su edición son lo principal,** con un nivel de cuidado como el de Rocambolesc.
- Detalle en `04_Contenido/reglas_de_contenido.md`, sección 0.

## Reglas que no se rompen nunca (pedido de Lauti)

- **Que no parezca hecho con IA.** Las piezas tienen que ser estéticas, con algo artístico, prolijas y que funcionen en el feed.
- **Sin degradés.**
- **Sin comillas.**
- **Sin guiones ni rayas** en los textos de las piezas ni en los textos de las publicaciones.
- **Un solo peso tipográfico por renglón:** nunca ExtraBold y Regular en la misma línea.
- **Sin paréntesis.**
- **Solo** los 6 colores y las 3 tipografías del manual.
- **Siempre siguiendo el manual de marca**, en cada pieza.
- **Siempre con el contexto:** Salta, el calor, el producto tucumano, dos amigos y un tono cercano.

## Imágenes generadas

Solo cuando sea realmente necesario. Lauti dio un token de Hugging Face para esos casos: **se le pide de nuevo, no se guarda en ningún archivo.** Una imagen generada nunca se presenta como foto real del producto.

## Otras reglas

- **WhatsApp:** nunca se manda nada sin que Lauti lo pida (regla global).
- **Idioma:** español rioplatense con voseo y tonada del norte.
