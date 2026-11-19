"""Cotizador de achilata. para eventos.

Calcula el precio al cliente, lo que hay que llevar y el margen de cada evento.

Uso:
    python cotizador.py --paquete clasico --invitados 100 --zona 1
    python cotizador.py --paquete fiesta --invitados 180 --zona 2 --horas-extra 1
    python cotizador.py --paquete empresa --invitados 60 --costo-kg 7000

Paquetes: clasico, fiesta, empresa, cumple, club_cerrado.
Los parámetros de abajo son los únicos que hay que tocar cuando cambien los precios.
"""

import argparse
import math

# Precios al cliente, en pesos. Vigentes hasta el 31/12/2026.
PAQUETES = {
    "clasico": {"nombre": "Clásico", "por_invitado": 5500, "minimo": 60, "horas": 2.0},
    "fiesta": {"nombre": "Fiesta", "por_invitado": 6800, "minimo": 80, "horas": 3.0},
    "empresa": {"nombre": "Empresa", "por_invitado": 4800, "minimo": 50, "horas": 2.0},
    "cumple": {"nombre": "Cumple", "precio_cerrado": 220000, "incluidos": 40,
               "extra": 4500, "horas": 1.5},
    "club_cerrado": {"nombre": "Club cerrado", "por_invitado": 3500, "minimo": 80, "horas": 2.0},
}
DESCUENTOS = [(250, 0.12), (150, 0.08)]          # desde N invitados, descuento
HORA_EXTRA = {"hasta_150": 90000, "mas_de_150": 120000}
ZONAS = {1: 0, 2: 45000}                          # zona 3 se cotiza aparte
RECARGO_FECHA_ESPECIAL = 0.25                     # 24/12 y 31/12

# Consumo y costos. Reemplazar con los datos reales apenas se tengan.
PORCION_KG = 0.12              # un vasito servido, a pesar en la prueba
PORCIONES_POR_HORA = 0.75      # porciones por invitado por hora de servicio
TOPE_PORCIONES = 2.2           # nadie come más que esto, aunque el servicio sea largo
MARGEN_SEGURIDAD = 0.20        # llevar 20 % más de lo calculado
COSTO_KG = 6000                # SUPUESTO, confirmar con el proveedor
COSTO_SET_VASITO = 200         # vasito de cartón, cucharita y servilleta
COSTO_FRIO = 20000             # hielo seco o hielo por evento
COSTO_TRASLADO = 15000         # combustible zona 1
COSTO_INSUMOS = 8000           # bolsas, guantes, limpieza


def pesos(n):
    return "$" + f"{round(n):,}".replace(",", ".")


def cotizar(paquete, invitados, zona=1, horas_extra=0, fecha_especial=False,
            lanzamiento=False, costo_kg=COSTO_KG):
    p = PAQUETES[paquete]
    horas = p["horas"] + horas_extra

    if paquete == "cumple":
        extra_inv = max(0, invitados - p["incluidos"])
        base = p["precio_cerrado"] + extra_inv * p["extra"]
        descuento = 0.0
    else:
        cobrados = max(invitados, p["minimo"])
        descuento = next((d for desde, d in DESCUENTOS if invitados >= desde), 0.0)
        base = cobrados * p["por_invitado"] * (1 - descuento)

    hora_extra = horas_extra * (HORA_EXTRA["mas_de_150"] if invitados > 150
                                else HORA_EXTRA["hasta_150"])
    if zona not in ZONAS:
        raise SystemExit("La zona 3 se cotiza aparte, con viáticos y alojamiento.")
    traslado = ZONAS[zona]

    total = base + hora_extra + traslado
    if fecha_especial:
        total *= 1 + RECARGO_FECHA_ESPECIAL
    if lanzamiento:
        total *= 0.80

    porciones_por_inv = min(PORCIONES_POR_HORA * horas, TOPE_PORCIONES)
    porciones = math.ceil(invitados * porciones_por_inv)
    kg = math.ceil(porciones * PORCION_KG * (1 + MARGEN_SEGURIDAD))
    vasitos = math.ceil(porciones * 1.1)

    costo = (kg * costo_kg + vasitos * COSTO_SET_VASITO + COSTO_FRIO
             + COSTO_TRASLADO * (1 if zona == 1 else 2.5) + COSTO_INSUMOS)
    ganancia = total - costo

    return {
        "paquete": p["nombre"], "invitados": invitados, "horas": horas,
        "descuento": descuento, "base": base, "hora_extra": hora_extra,
        "traslado": traslado, "total": total, "sena": total / 2,
        "porciones": porciones, "kg": kg, "vasitos": vasitos,
        "costo": costo, "ganancia": ganancia, "margen": ganancia / total,
        "por_invitado_final": total / invitados,
    }


def imprimir(r):
    print(f"\nPaquete {r['paquete']} · {r['invitados']} invitados · {r['horas']:g} h")
    print("-" * 46)
    print(f"Servicio            {pesos(r['base'])}"
          + (f"  con {r['descuento']:.0%} de descuento" if r["descuento"] else ""))
    if r["hora_extra"]:
        print(f"Horas extra         {pesos(r['hora_extra'])}")
    print(f"Traslado            {pesos(r['traslado']) if r['traslado'] else 'incluido'}")
    print(f"TOTAL AL CLIENTE    {pesos(r['total'])}")
    print(f"Seña 50 %           {pesos(r['sena'])}")
    print(f"Por invitado        {pesos(r['por_invitado_final'])}")
    print("\nPara llevar")
    print(f"Porciones estimadas {r['porciones']}")
    print(f"Achilata            {r['kg']} kg, con 20 % de margen")
    print(f"Vasitos             {r['vasitos']}")
    print("\nNúmeros internos, no se muestran al cliente")
    print(f"Costo estimado      {pesos(r['costo'])}")
    print(f"Ganancia            {pesos(r['ganancia'])}  ·  margen {r['margen']:.0%}\n")


if __name__ == "__main__":
    a = argparse.ArgumentParser(description="Cotizador de achilata. para eventos")
    a.add_argument("--paquete", choices=PAQUETES, default="clasico")
    a.add_argument("--invitados", type=int, required=True)
    a.add_argument("--zona", type=int, default=1)
    a.add_argument("--horas-extra", type=float, default=0)
    a.add_argument("--fecha-especial", action="store_true", help="24/12 o 31/12")
    a.add_argument("--lanzamiento", action="store_true", help="20 % de los 5 primeros")
    a.add_argument("--costo-kg", type=int, default=COSTO_KG)
    x = a.parse_args()
    imprimir(cotizar(x.paquete, x.invitados, x.zona, x.horas_extra,
                     x.fecha_especial, x.lanzamiento, x.costo_kg))
