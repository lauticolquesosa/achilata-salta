# 09 · Página web de achilata.

**La web está publicada en https://achilata-salta.vercel.app**, en Vercel, con la cuenta de Lauti, proyecto `achilata-salta`.

Es una web de varias páginas, hecha desde cero el 19/11/2026:
- Inicio con el pote de achilata en 3D que se mueve con el scroll.
- Qué es la achilata, con un pote 3D que se gira con el dedo.
- Precios y armador de pedidos.
- **Hacer un pedido, `pedir.html`, el enlace para la bio de Instagram.** Potes, día y turno de entrega, zona, dirección y pago, con el pedido mínimo. Los turnos y las reglas se cambian en `datos.json`, en `turnos` y `pedidos`: `dias` va de 0, domingo, a 6, sábado; `cierre` es la hora límite del mismo día en Salta; con `"dias": []` el turno se cierra. Se prueba con `node probar_pedir.mjs carpeta`, con el sitio servido. Sale del plan de turnos del 24/11/2026.
- Servicio para eventos.
- Calculadora de presupuesto.
- Las páginas legales: privacidad, cookies, términos con botón de arrepentimiento, y seguridad.
- La página de error.

Todo manda a WhatsApp. No hay servidor ni base de datos.

## Las carpetas

| Carpeta | Qué tiene |
|---|---|
| `sitio/` | **Lo que se publica.** Se genera solo: no se edita a mano |
| `fuente/` | Donde se trabaja: las páginas, las partes compartidas, el CSS, el JavaScript y los datos |
| `fuente/src/datos.json` | **La única fuente de los precios, teléfonos, zonas y paquetes.** Si cambia un precio, se cambia acá y se vuelve a generar |
| `fuente/paginas/` | Una página por archivo, con sus textos |
| `fuente/partes/` | La cabecera, el pie con lo legal y el aviso de cookies, compartidos por todas las páginas |
| `_archivo_web_eventos_v1/` | La primera web, solo de eventos, que estaba en `08_Eventos/06_Pagina_web`. Queda de referencia, y sus fotos las usa la propuesta en PDF |

## Cómo cambiar algo y volver a publicar

Desde `09_Pagina_web/fuente`, en Git Bash:

```
npm install            # solo la primera vez
node build.mjs         # genera sitio/ con los cambios
```

**Desde el 20/11/2026 la web se publica sola con cada push a main del repo.** Vercel toma la carpeta `09_Pagina_web/sitio`, así que alcanza con generar, hacer commit y push. Ese día un push publicó la raíz del repo y la web dio error 404; por eso se fijó la carpeta raíz del proyecto en Vercel. Para volver a publicar sin push: `npx vercel redeploy` con la última URL y `--target production`.

- Si cambian las fotos o los logos, antes de `node build.mjs` correr `python assets.py`. Pasa las fotos de `06_Assets` a AVIF y WebP en dos tamaños.
- Si cambian los precios de eventos, también hay que cambiarlos en `08_Eventos/03_Servicio_y_precios/cotizador.py` y en la propuesta en PDF.

## Cómo revisar antes de publicar

1. Servir `sitio/` en la compu, en `http://127.0.0.1:8765`.
2. Correr `node revisar.mjs carpeta-de-capturas`. Busca errores, violaciones de seguridad, desbordes y comillas, guiones o paréntesis en los textos. Además saca capturas de cada página en celular y escritorio.
3. Correr `node probar.mjs`. Son 30 pruebas: la calculadora contra el cotizador, el pedido, las validaciones, las cookies, el menú, el modo sin movimiento y la web sin JavaScript.
4. Correr `node capturar.mjs carpeta [url]`. Saca capturas de la portada a lo largo del tiempo.

## Resultados al publicar, 19/11/2026

| Prueba | Resultado |
|---|---|
| Seguridad, Mozilla Observatory | **A+, 155 puntos, 12 de 12** |
| Lighthouse, accesibilidad, buenas prácticas y SEO | **100** en las 9 páginas, en celular |
| Lighthouse, rendimiento en celular | De 91 a 98 según la página |
| Lighthouse, rendimiento del inicio en escritorio | 100 |
| Pruebas de funcionamiento | 30 de 30 |

## Cómo funciona por dentro

- **Seguridad:**
  - Política de contenido estricta: solo se ejecuta el código propio, autorizado por su hash. Además rige Trusted Types.
  - HTTPS obligatorio, y la web no se puede meter dentro de otra.
  - Permisos del navegador apagados.
  - Nada de código ni fuentes de terceros.
  - No hay claves ni contraseñas en ningún archivo.
  - Las cabeceras están en `sitio/vercel.json` y en `sitio/_headers`, para Netlify o Cloudflare.
  - La política de cómo reportar problemas está en `sitio/.well-known/security.txt`.
- **Privacidad:**
  - No usa cookies.
  - Solo guarda en el navegador la elección de privacidad, por 12 meses, y si ya se vio la bienvenida.
  - Los formularios no mandan nada a ningún servidor: arman el mensaje de WhatsApp en el celular de quien escribe.
  - Las políticas siguen la Ley 25.326 e incluyen la leyenda obligatoria de la AAIP.
  - Están el botón de arrepentimiento y el enlace a Defensa del Consumidor.
- **El 3D:**
  - Es un pote de achilata generado con código en three.js, sin descargar modelos.
  - Desde el 20/11/2026 es fiel a las fotos: un pote de papel con el logo y la bajada impresos, y tres bochas fucsia con el granulado del hielo raspado. El granulado se calcula por píxel en la placa de video. Sin palito ni gotas.
  - En el inicio el 3D es lo único: no hay foto encima. Se arma apenas carga la página.
  - La foto queda solo de respaldo, si el equipo no puede mostrar 3D.
  - La posición del pote sale de una tabla de poses en `main.js`, POSES, según cuánto se bajó. No usa animaciones encadenadas, así al volver arriba queda siempre igual. En el celular sube pegado al inicio y se desvanece.
  - Si la persona pidió menos movimiento en su sistema, el pote queda quieto.
- **Tipografía:**
  - Escala reducida el 20/11/2026, tomando como base sitios como Apple, Stripe, Linear y Vercel.
  - Texto de 16 a 18 px y menú y botones de 16 px.
  - Títulos de sección de 34 a 72 px y título principal de 44 a 120 px.
  - Sobre rojo, el texto va en ExtraBold de 19 px para que el contraste siga cumpliendo.
- **Animaciones:**
  - GSAP con ScrollTrigger y scroll suave con Lenis.
  - Títulos que suben por líneas, fotos que se abren, collage con parallax y la foto de eventos que se abre a pantalla completa.
  - Una galería horizontal fija, los paquetes que se apilan, la línea de los pasos que se dibuja y los precios que cuentan.
  - Transiciones entre páginas.
  - No hay marquesinas infinitas ni cambios de color dentro de un renglón.
- **SEO y buscadores con IA:**
  - Datos estructurados del negocio, el producto, el servicio y las preguntas frecuentes.
  - `sitemap.xml` y `robots.txt` con permiso para los buscadores con IA.
  - `llms.txt` con el resumen del negocio para ChatGPT, Claude y Perplexity.

## Pendientes

1. **Dominio propio.** Hoy es `achilata-salta.vercel.app`. Si compran `achilatasalta.com.ar` en NIC Argentina:
   - Se conecta en Vercel.
   - Se cambia `dominio` en `datos.json` y se vuelve a publicar.
2. **Revisión legal.** Las políticas siguen la ley argentina, pero conviene que las lea un abogado antes de vender en serio, sobre todo arrepentimiento y cancelaciones.
3. **Data fiscal de ARCA.** Cuando tengan el monotributo, sumar el QR de Data Fiscal en el pie.
4. **Fotos reales.** Las fotos actuales son las de `06_Assets`, y la web aclara que son ilustrativas. Cuando haya fotos del carrito en un evento, sumarlas.
5. **Salsa de leche condensada del paquete Fiesta.** La web la ofrece. Probarla antes del primer evento que la contrate.
6. **Medición de visitas.** Hoy no hay ninguna. Si se suma, tiene que cargarse solo con el permiso del aviso de cookies, usando `permite("medicion")` de `src/consent.js`.
