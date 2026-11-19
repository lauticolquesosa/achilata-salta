# Cronograma de dos semanas de @achilatasalta, del jueves 19/11 al miércoles 2/12/2026.
# Es la única fuente: de acá salen el .md, las carpetas de piezas y el PDF. Uso: python generar.py
# Es una base, no algo fijo. Los pedidos del día se hacen igual y el cronograma se acomoda: ver COMO_FUNCIONA.
# Reglas de los textos: sin guiones, sin comillas y sin paréntesis.

INICIO = (2026, 11, 19)
N_DIAS = 14

# Cada pieza: (título, tipo, formato, cómo es, texto de la publicación)
PIEZAS = {
 "P01": ("Hay achilata en Salta", "Publicación", "Carrusel de 5 placas",
  "La primera publicación desde la vuelta. Todo en el estudio rojo: cada foto pasada al rojo achilata con su luz y su sombra reales, y títulos blancos pesados. "
  "Placa 1: la palma que presenta el vasito, con Hay achilata en Salta pisado por la bocha. "
  "Placa 2: la cuchara que levanta, con la historia del nombre, hay gelata. "
  "Placa 3: la bocha de cerca, con Hielo raspado. Color fucsia. Receta tucumana. "
  "Placa 4: el vaso con tres bochas, con Potes de 1 kg y medio kilo. "
  "Placa 5: rojo con el logo blanco, los dos WhatsApp, las zonas y el pago.",
  "Volvimos y llegamos a Salta 🍧 El helado más tucumano, ahora a la vuelta de tu casa. Potes de 1 kg y medio kilo, pedidos por WhatsApp. ¿Vos ya la probaste?"),
 "P02": ("El menú", "Publicación", "Carrusel de 3 placas",
  "Una plantilla fija que después se repite cada vez que haya que recordar los precios. "
  "Placa 1: crema, el pote de 1 kg al centro, arriba 1 KG en ExtraBold rojo y abajo $12.000. "
  "Placa 2: la misma composición con MEDIO KILO y $8.000. "
  "Placa 3: bordó, con cómo pedir, las zonas, transferencia o efectivo y los dos WhatsApp.",
  "Dos tamaños y un solo sabor, el de siempre. Guardalo para cuando apriete el calor ☀️"),
 "R01": ("El ritual", "Reel", "Video vertical de 7 a 10 segundos",
  "Sin hablar. Primer plano de la cuchara entrando en el pote y sirviendo una copa, con el sonido real del hielo. "
  "La portada es un cuadro de la copa llena con El ritual en ExtraBold crema. "
  "Si no hay video real, se arma con fotos de la galería en movimiento suave o se cambia por una publicación de producto.",
  "Así se sirve una achilata de verdad. Subí el volumen 🔊"),
 "P04": ("Hace 32 grados", "Publicación", "Placa única",
  "Solo tipografía, con mucho aire. Crema, y en ExtraBold bordó alineado a la izquierda: Hace 32 grados en Salta y vos todavía no probaste achilata. "
  "El logo reducido chico en una esquina. Si ese día hace otra temperatura, se cambia el número por el real.",
  "Lo arreglamos hoy mismo. Pedí tu pote por WhatsApp ☀️"),
 "P07": ("La siesta salteña", "Publicación", "Foto única",
  "La foto más luminosa de la galería: una mano con el pote o la copa al sol, con fondo de cielo, árboles o calle. "
  "Sin texto encima, solo el logo reducido chico. Es la publicación que le da aire a la grilla después de una placa de texto.",
  "El postre oficial de la siesta salteña ☀️ ¿Vos desde dónde la comés?"),
 "P08": ("Achilata, sustantivo", "Publicación", "Placa única",
  "Como una entrada de diccionario sobre crema: achilata en ExtraBold rojo, debajo sustantivo femenino en Regular y la definición: "
  "helado de agua tucumano, color fucsia, hecho de hielo raspado. Se come con calor y en buena compañía.",
  "Para los que todavía preguntan qué es 🍧 Mandáselo a ese amigo que no la conoce."),
 "R03": ("La textura", "Reel", "Video vertical de 6 segundos en loop",
  "Primer plano de la cuchara entrando en el hielo fucsia, en cámara lenta. Sin texto o con una sola palabra: Hielo. "
  "Si no hay video, se hace con el primer plano de la galería y un movimiento de cámara lento.",
  "Esto es lo que tenés que ver cuando hace 32 grados ☀️"),
 "P03": ("Zonas de delivery", "Publicación", "Placa única",
  "Un mapa simple de Salta dibujado en bordó sobre crema, con las zonas marcadas en rojo: Grand Bourg, San Lorenzo Chico, San Lorenzo, El Tipal y La Almudena. "
  "Abajo: ¿Tu zona no está? Consultanos.",
  "Llegamos a Grand Bourg, San Lorenzo Chico, San Lorenzo, El Tipal y La Almudena. Si estás en otra zona, escribinos y lo vemos 🍧"),
 "P10": ("La achilata anotada", "Publicación", "Foto con anotaciones",
  "Rojo pleno con el pote o la copa al centro, recortado y con su sombra real. Alrededor, en Regular crema y con líneas finas: "
  "hielo raspado, color fucsia, receta tucumana, sabor clásico, potes de 1 kg y medio kilo.",
  "Todo lo que tiene una achilata, en una foto. ¿Le falta algo?"),
 "P06": ("Este finde hay achilata", "Publicación", "Placa con goteo",
  "El fondo de goteo rojo sobre gofre bordó del manual. En la zona del gofre, en crema: Este finde hay achilata. "
  "Debajo, en una línea: pedidos por WhatsApp hasta el viernes a la noche.",
  "Arrancamos a tomar pedidos para el finde. Escribinos y te lo llevamos 🍧"),
 "P09": ("Cómo pedir", "Publicación", "Carrusel de 5 placas",
  "Para guardar. Portada rosa con el producto y el título enorme Cómo pedir. "
  "Placa 2: Elegí tu tamaño, 1 kg o medio kilo. Placa 3: Escribinos por WhatsApp con tu zona. "
  "Placa 4: Pagá por transferencia o en efectivo. Placa 5: rojo con los dos números.",
  "Guardalo y la próxima te sale en un minuto. Pedidos por WhatsApp 🍧"),
 "R04": ("Así sale tu pedido", "Reel", "Video vertical de 10 a 15 segundos",
  "Detrás de escena real: los dos preparando y cerrando potes, la conservadora y la salida a entregar. Cortes rápidos con música. "
  "Texto en pantalla: Así sale tu pedido. Este necesita video propio.",
  "Del freezer a tu casa 🍧 Gracias por cada pedido."),
 "P05": ("No deslices", "Publicación", "Carrusel de 5 placas",
  "Placa 1: crema, solo NO DESLICES en ExtraBold bordó. Placas 2 a 4, la misma tipografía cada vez más grande: En serio. Te vas a tentar. Última oportunidad. "
  "Placa 5: la mejor foto de producto de la galería con Bueno, vos te la buscaste.",
  "Te dijimos que no deslices 🍧 Etiquetá a quien le debés una achilata."),
 "R02": ("Primera vez", "Reel", "Video vertical de 10 a 20 segundos",
  "Un salteño prueba achilata por primera vez, sin guion, con su reacción real. Texto en pantalla en una línea: Un salteño prueba achilata por primera vez. "
  "Este necesita video propio; si no hay, se cambia por otra publicación.",
  "¿Vos te acordás de tu primera achilata? 🍧"),
 "P11": ("Etiquetá a quien le debés", "Publicación", "Placa única",
  "Bordó con texto crema grande: Etiquetá a quien le debés una achilata. Debajo, en Ink Free rosa: y pagá la deuda este finde.",
  "Etiquetalo acá abajo 👇 Si te etiquetan, ya sabés lo que te toca."),
 "P12": ("Lo que nos escriben", "Publicación", "Placa única o carrusel",
  "Capturas reales de mensajes de clientes del primer y segundo finde, con permiso, limpias y centradas sobre crema. Arriba, chico: Lo que nos escriben. "
  "Si todavía no hay mensajes, va una foto de producto con una frase.",
  "Gracias por cada mensaje 🩷 Seguimos llevando achilata a toda la zona."),
 "P16": ("Salta en diciembre", "Publicación", "Placa única",
  "Rojo pleno con el texto crema enorme: Salta en diciembre. Ninguna explicación más. El logo reducido chico.",
  "Ya sabés qué hacer ☀️ Pedidos por WhatsApp."),
 "R06": ("Nosotros", "Reel", "Video vertical o carrusel de fotos",
  "Los dos socios en cámara, con los potes: quiénes son, por qué achilata y de dónde viene. Sus nombres escritos a mano en Ink Free. "
  "Si no hay video, va como carrusel de fotos de ustedes dos.",
  "Somos los que te llevan la achilata 🩷 Encantados."),
}

# Cada día: tema, objetivo, feed [(hora, código)], historias [(hora, texto)], nota
DIAS = {
 1: ("La vuelta", "Contar que volvimos y que la achilata llegó a Salta, y enamorar con el producto en un segundo.",
     [("20.00", "P01")],
     [("19.30", "Volvimos. La bocha que cae al vaso, en el estudio rojo."),
      ("20.05", "Nueva publicación. Se comparte la portada de P01 sobre rojo."),
      ("20.30", "Precios: 1 kg a $12.000 y medio kilo a $8.000."),
      ("21.00", "Encuesta: ¿Ya probaste achilata? Con las opciones Sí, la amo 🩷 y ¿Qué es eso?"),
      ("22.00", "Pedidos por WhatsApp. Los dos números, las zonas y el sticker de enlace.")],
     "Antes de publicar: foto de perfil, presentación, enlaces y destacadas listas. En la primera hora se responden todos los comentarios y se fija uno propio: ¿Desde qué barrio nos escribís?"),
 2: ("Precios claros", "Que quede claro cuánto sale y cómo se pide, para llegar al primer finde con pedidos.",
     [("13.00", "P02")],
     [("11.00", "Tomamos pedidos para el finde."),
      ("13.05", "Se comparte El menú."),
      ("17.00", "Pregunta: ¿En qué zona estás? Sirve para ver dónde está la gente."),
      ("19.00", "Quiz: ¿De dónde viene el nombre? Hay gelata, un pueblo o un helado italiano."),
      ("21.30", "Recordatorio: pago por transferencia o en efectivo.")],
     ""),
 3: ("Primer sábado de venta", "Vender. Todo el día gira alrededor del pedido.",
     [("13.00", "R01"), ("20.00", "P04")],
     [("10.30", "Buen día, hoy hay achilata."),
      ("12.00", "Tomamos pedidos para hoy."),
      ("13.05", "Se comparte El ritual."),
      ("16.00", "Deslizador: ¿Cuánto calor hace hoy?"),
      ("18.00", "Entregas en vivo, con fotos o videos reales del día."),
      ("20.05", "Se comparte Hace 32 grados."),
      ("22.00", "Gracias Salta, al cierre.")],
     "El día más fuerte de la primera semana. Los reposts de clientes que etiquetan se comparten apenas llegan."),
 4: ("Domingo de siesta", "Vender el postre del domingo y cerrar el primer finde.",
     [("13.00", "P07")],
     [("11.00", "Domingo de siesta."),
      ("13.05", "Se comparte La siesta salteña."),
      ("15.00", "Encuesta: ¿1 kg o medio kilo?"),
      ("18.00", "Reposts de clientes."),
      ("21.30", "Cierre del primer finde, con un gracias.")],
     ""),
 5: ("Qué es la achilata", "Explicarle al salteño que no la conoce qué es, con humor.",
     [("20.00", "P08")],
     [("12.00", "Resumen del finde."),
      ("20.05", "Se comparte Achilata, sustantivo."),
      ("21.00", "Pregunta: ¿Qué querés ver por acá?")],
     "Lunes tranquilo: pocas historias y una pieza para guardar y compartir."),
 6: ("La textura", "Mostrar el producto de cerca: el hielo, el color, el frío.",
     [("20.00", "R03")],
     [("13.00", "Detrás de escena, algo simple del día."),
      ("20.05", "Se comparte La textura."),
      ("21.00", "Encuesta: ¿Con cuchara o directo del pote?")],
     ""),
 7: ("Dónde llegamos", "Que cada uno sepa si llegamos a su zona antes de abrir los pedidos.",
     [("20.00", "P03")],
     [("13.00", "Quiz: ¿Cuántas copas salen de un kilo?"),
      ("20.05", "Se comparte Zonas de delivery."),
      ("21.30", "Mañana abrimos pedidos para el finde.")],
     ""),
 8: ("Abrimos pedidos", "Arrancar el segundo finde con pedidos anotados desde el jueves.",
     [("13.00", "P10"), ("20.00", "P06")],
     [("11.00", "Abrimos pedidos para el finde."),
      ("13.05", "Se comparte La achilata anotada."),
      ("18.00", "Pregunta: ¿Para qué día querés tu pote?"),
      ("20.05", "Se comparte Este finde hay achilata."),
      ("21.30", "Recordatorio de precios.")],
     ""),
 9: ("Viernes de pedidos", "Facilitar el pedido y mostrar que detrás hay dos personas reales.",
     [("13.00", "P09"), ("20.00", "R04")],
     [("11.00", "Tomamos pedidos para hoy y mañana."),
      ("13.05", "Se comparte Cómo pedir."),
      ("16.00", "Preparando pedidos, en vivo."),
      ("19.00", "Encuesta: ¿Copa o directo del pote?"),
      ("20.05", "Se comparte Así sale tu pedido."),
      ("22.00", "Reposts de clientes.")],
     ""),
 10: ("Segundo sábado", "El día de más venta de las dos semanas.",
     [("13.00", "P05"), ("20.00", "R02")],
     [("10.30", "Buen día, hoy hay achilata."),
      ("12.00", "Tomamos pedidos para hoy."),
      ("13.05", "Se comparte No deslices."),
      ("16.00", "Deslizador: ¿Cuánto calor hace hoy?"),
      ("18.00", "Entregas en vivo."),
      ("20.05", "Se comparte Primera vez."),
      ("22.00", "Gracias por hoy.")],
     ""),
 11: ("Domingo para compartir", "Que nos etiqueten y la cuenta llegue a gente nueva.",
     [("13.00", "P11")],
     [("11.00", "Domingo de siesta."),
      ("13.05", "Se comparte Etiquetá a quien le debés."),
      ("15.00", "Pregunta: ¿Con quién la compartís?"),
      ("18.00", "Reposts de clientes."),
      ("21.30", "Cierre del segundo finde.")],
     ""),
 12: ("Lo que nos escriben", "Mostrar que a la gente le gustó, con mensajes reales.",
     [("20.00", "P12")],
     [("12.00", "Resumen del finde."),
      ("20.05", "Se comparte Lo que nos escriben."),
      ("21.00", "Encuesta: ¿Más pedidos el finde o también en la semana?")],
     "Juntar durante el finde capturas de mensajes lindos, siempre con permiso."),
 13: ("Arranca diciembre", "Instalar que diciembre en Salta es achilata.",
     [("20.00", "P16")],
     [("11.00", "Diciembre arranca."),
      ("20.05", "Se comparte Salta en diciembre."),
      ("21.00", "Quiz sobre la achilata.")],
     ""),
 14: ("Nosotros", "Ponerle cara a la marca antes del tercer finde.",
     [("20.00", "R06")],
     [("13.00", "Pregunta: Preguntanos lo que quieras."),
      ("20.05", "Se comparte Nosotros."),
      ("21.30", "Mañana abrimos pedidos para el finde.")],
     "Para este día hacen falta fotos o video de ustedes dos y sus nombres."),
}

COMO_FUNCIONA = [
 ("El cronograma es la base, no algo fijo",
  "Todos los días hay algo para subir, y de jueves a domingo hay más, porque son los días de venta. Pero cualquier día se puede pedir una pieza que no estaba: una historia con los precios, un aviso de lluvia, una promo o lo que haga falta. Se hace en el momento y el cronograma se acomoda solo."),
 ("Cómo se acomoda",
  "Si lo que se pide reemplaza algo que estaba previsto, por ejemplo una historia de precios el día que tocaba recordar los precios, lo previsto se saca o se mueve a otro día. Si se suma algo nuevo, lo demás queda igual. Si un día no se sube lo planeado, pasa al siguiente hueco libre o se descarta, sin romper el orden de la grilla."),
 ("Cada pieza se hace cuando se pide",
  "Las piezas no se arman todas por adelantado. Cuando se pide una, se revisa toda la galería de fotos, se elige la que mejor le queda, se estudia su luz, su color y su textura, se adapta al formato y se diseña siguiendo el manual. Así cada pieza sale con las mejores fotos que haya en ese momento."),
 ("Cuando la pieza está lista",
  "Se mandan al WhatsApp de Lauti todas las imágenes como documento, en orden, sin compresión, y después, en un mensaje aparte, el texto limpio para copiar y pegar en Instagram. Queda guardada en su carpeta y anotada en el registro de publicaciones."),
]
