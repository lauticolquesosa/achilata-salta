# P01 y H01 · versión 2 del 19/11/2026

La versión 1 no le gustó a Lauti y está en `_v1 descartada/`. Esta sigue las correcciones del 19/11 y el análisis 2d de `05_Referencias/analisis_de_referencias.md`.

## El estudio rojo
Todas las fotos se pasaron a un fondo rojo achilata #E7364A sin costuras:
- **El recorte** combina rembg con una máscara por color, y se corrige a mano cuando hace falta. Al vaso de la 11 se le reconstruyó la forma.
- **La luz del fondo original pasa al rojo:** su luminancia, con el producto sacado, multiplica al rojo. Así **la sombra de contacto y la caída de luz son las reales.**
- **Los bordes** se limpian del color del fondo viejo, para que no queden halos.
- **Los reflejos** amarillos de la cuchara de metal, en las fotos 02 y 13, se pasaron a rosa, que es lo que reflejaría sobre rojo.

Las herramientas están en `06_Assets/fotos/herramientas/`, y las fotos ya pasadas al estudio rojo, en `06_Assets/fotos/editadas/estudio rojo/`.

## Las piezas

| Pieza | Foto | Texto |
|---|---|---|
| P01 1 portada | 05, la palma que presenta el vasito | Hay achilata en Salta. La bocha pisa el título |
| P01 2 | 16, la cuchara que levanta | La historia del nombre |
| P01 3 | 10, la bocha en la cuchara de servir, de cerca | Hielo raspado. Color fucsia. Receta tucumana. |
| P01 4 | 11, el vaso con tres bochas | Potes de 1 kg y medio kilo. |
| P01 5 | Rojo liso con el logo | Pedidos, números, zonas y pago |
| H01 1, 19.30 | 02, la bocha que cae al vaso | Volvimos. |
| H01 2, 20.05 | Rojo liso | Nueva publicación |
| H01 3, 20.30 | 07, con luz de ventana | Precios |
| H01 4, 21.00 | 13, espejada | Encuesta |
| H01 5, 22.00 | Rojo liso | Pedidos |

- **Títulos:** Bricolage ExtraBold blanca, con un borde del mismo color del 3 % del tamaño.
- **Logo:** sin bajada y blanco. Nunca la `a.`.
- **Bordó:** no se usó.

## Ajustes del 19/11, segunda ronda de correcciones
- **Recortes perfectos.**
  - La transparencia del borde se refina con un guided filter de color, que sigue el detalle real de la foto.
  - El color del producto en el borde se recupera con blur fusion, sin el fondo viejo.
  - Así no quedan halos ni bordes escalonados. Está en `06_Assets/fotos/herramientas/matte.py`.
- **Borde de los títulos:** bajó del 3 al 1,5 % del tamaño de la letra.
- **Placa 5, el cierre:** pasó a la foto 07, con Pedí la tuya. y los dos números en botones blancos, como hacen OddFellows y Morgenstern's.
- **Historia de precios:** Elegí tu pote., con dos tarjetas blancas, 1 kg a $12.000 y 1/2 kg a $8.000, sobre la foto 11.
- **Historia 2:** se suma una opción simple que ya trae la portada puesta.
