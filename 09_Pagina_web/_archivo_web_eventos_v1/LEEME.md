# Página web de eventos

`index.html` es una página única, lista para publicar. No necesita instalar nada.

## Qué tiene
- Inicio con la propuesta y la foto principal.
- Por qué achilata, qué incluye y para qué eventos.
- Los 5 paquetes con precios.
- Zonas y cómo reservar.
- **Calculadora de presupuesto:** el cliente elige paquete, invitados, fecha, zona y lugar, ve un estimado y manda todo armado por WhatsApp al 387 483 4041.
- Preguntas frecuentes y contacto.

## Cómo verla
Abrir `index.html` con doble clic en Chrome.

## Cómo publicarla
**Opción recomendada, gratis: GitHub Pages.** El repo ya es público.
1. En GitHub, ir a Settings, Pages.
2. Elegir la rama `main` y la carpeta raíz.
3. La web queda en `lauticolquesosa.github.io/achilata-salta/08_Eventos/06_Pagina_web/`.

**Con dominio propio:** comprar `achilatasalta.com.ar` en NIC Argentina y publicarla en Vercel o Netlify arrastrando la carpeta. El MCP de Vercel no conectó en esta sesión porque el token está vencido.

## Cuando cambien los precios
Hay que cambiarlos en tres lugares:
1. `03_Servicio_y_precios/cotizador.py`
2. `index.html`: las tarjetas de paquetes y el objeto `P` del script al final.
3. `04_Presentacion/fuente/propuesta.html`, y volver a generar el PDF.

## Fotos
Están en `img/`, sacadas de `06_Assets/fotos/`. **Cuando haya fotos reales de eventos, reemplazar `servicio.jpg` y `fila.jpg` por fotos del carrito en una fiesta.**
