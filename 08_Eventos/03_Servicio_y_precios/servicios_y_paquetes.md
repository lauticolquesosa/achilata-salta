# Servicios y precios · achilata. para eventos

**Lista de precios vigente del 19/11 al 31/12/2026.** En enero se revisa según la inflación y el costo del proveedor. Todos los precios en pesos, por evento.

Antes de publicar estos precios, Lauti confirma: el costo del kilo con el proveedor, el costo de los vasitos y el del carrito. Si alguno cambia mucho, se recalcula con `cotizador.py`.

---

## Qué incluye siempre, en cualquier paquete

- **El carrito o la estación de achilata** con la marca, armado y desarmado.
- **Dos personas atendiendo,** con uniforme de la marca.
- **Achilata libre** durante el horario contratado: cada invitado se sirve las veces que quiera.
- **Vasitos de cartón y cucharitas de madera,** servilletas y cesto de residuos propio.
- **Traslado dentro de la Zona 1.**
- **Frío asegurado** durante todo el servicio.
- **Llegamos 60 minutos antes** y dejamos el espacio limpio.

---

## Los paquetes

### 1. Clásico · casamientos, 15 y fiestas
**El servicio base para eventos sociales.**
- 2 horas de servicio, en el momento que elijan: después de la cena, en la trasnoche o en el postre.
- **$5.500 por invitado.**
- **Mínimo 60 invitados,** o sea $330.000.

### 2. Fiesta · el completo
**Para casamientos y fiestas de 15 donde quieren algo especial.**
- 3 horas de servicio.
- Todo lo del Clásico, más:
  - **Salsa de leche condensada** y dos toppings a elección **[a probar antes de ofrecer]**.
  - **Cartel con los nombres** o la fecha del evento, en la estética de la marca.
  - **Carrito iluminado** para la noche.
  - **Achilata en copa con espumante** para el brindis o la trasnoche **[a probar antes de ofrecer]**.
- **$6.800 por invitado.**
- **Mínimo 80 invitados,** o sea $544.000.

### 3. Empresa · fin de año, aniversarios y lanzamientos
- 2 horas de servicio, de día o de noche.
- Todo lo del Clásico.
- **Con factura.**
- Opcional: vasitos con el logo de la empresa junto al nuestro, a cotizar según cantidad.
- **$4.800 por invitado.**
- **Mínimo 50 invitados,** o sea $240.000.

### 4. Cumple · eventos chicos
**Cumpleaños, bautismos, comuniones y reuniones en casas y quintas.**
- 90 minutos de servicio.
- Hasta 40 invitados, entre chicos y grandes.
- **$220.000 precio cerrado.**
- Cada invitado extra, $4.500.

### 5. Club y torneo · venta al público
**Para torneos, partidos, ferias, corsos y eventos abiertos.** No cobra el organizador, cobramos a cada persona.
- **Vasito de achilata: $2.500.**
- **Dos vasitos: $4.500.**
- Al club u organizador le dejamos **un 10 % de lo vendido** o un monto fijo acordado, y achilata gratis para su staff o sus jugadores, a convenir.
- Si el club prefiere **invitar a los jugadores o delegaciones,** se cotiza como evento cerrado, a **$3.500 por persona** con mínimo de 80.

---

## Ajustes

**Por cantidad de invitados:**
| Invitados | Descuento sobre el precio por invitado |
|---|---|
| Hasta 149 | precio lista |
| 150 a 249 | 8 % |
| 250 o más | 12 % |

**Hora extra:**
- Hasta 150 invitados: **$90.000** la hora.
- Más de 150 invitados: **$120.000** la hora.
- Se pide en el momento o con anticipación. Si se pide en el momento, depende del stock que llevamos.

**Zonas de traslado:**
| Zona | Lugares | Costo |
|---|---|---|
| **Zona 1** | Salta Capital, San Lorenzo, Vaqueros, La Caldera, Cerrillos, La Merced. Hasta 25 km | Incluido |
| **Zona 2** | Chicoana, El Carril, Rosario de Lerma, Campo Quijano, General Güemes. De 25 a 70 km | **$45.000** |
| **Zona 3** | Cafayate, valles y el resto de la provincia | A cotizar, con viáticos y alojamiento |

**Días:**
- Los precios son iguales de lunes a domingo.
- **31/12 y 24/12: 25 % de recargo.**

---

## Reserva y pago

- **Seña del 50 %** para reservar la fecha. Sin seña, la fecha no queda tomada.
- **Saldo** hasta 7 días antes del evento.
- La cantidad final de invitados se confirma 7 días antes. Si aumenta, se cobra la diferencia. Si baja, se respeta el mínimo.
- **Pago por transferencia o en efectivo.** Con factura para empresas.
- Las condiciones completas están en `09_Operacion/condiciones_del_servicio.md`.

---

## Precio de lanzamiento

**Para los primeros 5 eventos, hasta el 15/12/2026: 20 % de descuento.**
- A cambio: permiso para sacar fotos y videos, y una reseña o un video corto de los anfitriones.
- Sirve para tener el material que nos falta para vender casamientos.
- **No se publica como descuento en redes.** Se ofrece uno a uno, a conocidos y al club. Nunca competimos por precio.

---

## Cómo se ve un presupuesto

Ejemplo: casamiento de 120 invitados en San Lorenzo, paquete Fiesta.

| Concepto | Monto |
|---|---|
| 120 invitados × $6.800 | $816.000 |
| Traslado Zona 1 | Incluido |
| **Total** | **$816.000** |
| Seña para reservar, 50 % | $408.000 |
| Saldo 7 días antes | $408.000 |

Para calcular cualquier presupuesto, correr:

```
python cotizador.py --paquete fiesta --invitados 120 --zona 1
```
