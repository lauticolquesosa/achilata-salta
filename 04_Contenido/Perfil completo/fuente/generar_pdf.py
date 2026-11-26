# Guía del perfil completo de @achilatasalta · 26/11/2026
# Rehace el PDF y textos_para_copiar.md. Uso: python generar_pdf.py
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate,Frame,PageTemplate,Paragraph,Spacer,Image,Table,TableStyle,PageBreak,KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from PIL import Image as PI

AQUI=os.path.dirname(os.path.abspath(__file__)); PC=os.path.dirname(AQUI); C=os.path.dirname(PC)
FD=r'C:\Users\Lauti\AppData\Local\Microsoft\Windows\Fonts'
pdfmetrics.registerFont(TTFont('XB',FD+r'\BricolageGrotesque-ExtraBold.ttf'))
pdfmetrics.registerFont(TTFont('RG',FD+r'\BricolageGrotesque-Regular.ttf'))
pdfmetrics.registerFont(TTFont('INK',r'C:\Windows\Fonts\Inkfree.ttf'))
ROJ=HexColor('#E7364A'); CRE=HexColor('#FFF3E2'); BOR=HexColor('#3A1320'); ROSA=HexColor('#F3A3B5')

H1=ParagraphStyle('h1',fontName='XB',fontSize=30,leading=31,textColor=ROJ,spaceAfter=10)
H2=ParagraphStyle('h2',fontName='XB',fontSize=17,leading=20,textColor=ROJ,spaceBefore=12,spaceAfter=5)
TX=ParagraphStyle('tx',fontName='RG',fontSize=10.5,leading=14.5,textColor=BOR,spaceAfter=5)
CH=ParagraphStyle('ch',fontName='RG',fontSize=9,leading=12,textColor=BOR)
NO=ParagraphStyle('no',fontName='INK',fontSize=13,leading=16,textColor=ROJ,spaceAfter=6)
CP=ParagraphStyle('cp',fontName='RG',fontSize=9.5,leading=13,textColor=BOR,backColor=HexColor('#FFFFFF'),borderPadding=7,spaceBefore=6,spaceAfter=12)
def P(t,s=TX): return Paragraph(t,s)
def bul(items): return [P('•&nbsp;&nbsp;'+i) for i in items]
import tempfile,hashlib
CACHE=os.path.join(tempfile.gettempdir(),'achilata_pdf_cache'); os.makedirs(CACHE,exist_ok=True)
def img(path,w):
    im=PI.open(path).convert('RGB'); px=round(w/mm*12)   # unos 300 dpi
    if im.width>px: im=im.resize((px,round(im.height*px/im.width)),PI.LANCZOS)
    j=os.path.join(CACHE,hashlib.md5(path.encode()).hexdigest()+'.jpg'); im.save(j,quality=86)
    return Image(j,width=w,height=w*im.height/im.width)

PU=C+r'\Publicaciones'; RE=C+r'\Reels'; DE=C+r'\Destacadas'; PX=C+r'\Historias\Próximas historias'

# ---------- las 10 publicaciones nuevas, en orden ----------
PUBS=[
 ('1','jue 26/11 13.00','Carrusel de 4','P08 Achilata, sustantivo',PU+r'\P08 Achilata, sustantivo\final','P08 1 achilata.png',
  'Achilata. Sustantivo femenino. Helado de agua tucumano, fucsia, frío y de cuchara.\n\nDicen que el nombre viene de los heladeros italianos que gritaban hay gelata. Nosotros la trajimos a Salta para que no tengas que viajar a Tucumán.\n\nPedí por WhatsApp al 387 483 4041 o al 387 468 4498.'),
 ('2','jue 26/11 20.00','Reel de 12 s','R03 La textura',RE+r'\R03 La textura\final','R03 portada.png',
  'Mirá esta textura. Hielo raspado, color fucsia y receta tucumana.\n\nAsí llega a tu casa, en pote de 1 kg o de medio kilo. Pedidos por WhatsApp, link en la bio.'),
 ('3','vie 27/11 13.00','Placa única','P04 Hace 32 grados',PU+r'\P04 Hace 32 grados\final','P04 1 hace 32.png',
  'Hace 32 grados en Salta y vos todavía sin achilata. Lo arreglamos rápido: escribinos y te la llevamos bien fría.\n\n1 kg a $12.000\nMedio kilo a $8.000\n387 483 4041 o 387 468 4498'),
 ('4','vie 27/11 20.00','Carrusel de 6','P09 Cómo pedir',PU+r'\P09 Cómo pedir\final','P09 1 portada.png',
  'Guardalo para el finde. Cómo pedir tu achilata en cuatro pasos:\n\n1. Escribinos por WhatsApp.\n2. Elegí tu pote, 1 kg o medio kilo.\n3. Pasanos tu zona.\n4. Pagá con transferencia o efectivo.\n\nY te la llevamos fría. Envíos a Grand Bourg, San Lorenzo Chico, San Lorenzo, El Tipal y La Almudena. Si estás en otra zona, consultanos.'),
 ('5','sáb 28/11 13.00','Reel de 8 s','R01 Una cucharada',RE+r'\R01 El ritual\final','R01 portada.png',
  'Una cucharada y estás en Tucumán. Para los tucumanos que la extrañan y para los salteños que todavía no la probaron.\n\nPedí la tuya al 387 483 4041 o al 387 468 4498.'),
 ('6','sáb 28/11 20.00','Placa única','P11 Etiquetá a quien le debés',PU+r'\P11 Etiquetá a quien le debés\final','P11 1 etiqueta.png',
  'Etiquetá a quien le debés una achilata. Y que pague esta vez.\n\nPotes de 1 kg y medio kilo con envío. Pedidos por WhatsApp, link en la bio.'),
 ('7','dom 29/11 20.00','Carrusel de 5','P05 No deslices',PU+r'\P05 No deslices\final','P05 1 no deslices.png',
  'Te dijimos que no deslices. Bueno, vos te lo buscaste.\n\nAhora pedí la tuya por WhatsApp al 387 483 4041 o al 387 468 4498. 1 kg a $12.000 y medio kilo a $8.000.'),
 ('8','lun 30/11 20.00','Placa única','P10 La achilata anotada',PU+r'\P10 La achilata anotada\final','P10 1 anotada.png',
  'La achilata, anotada. Hielo raspado, receta tucumana, sabor clásico y un pote de 1 kg que llega frío a tu casa.\n\nContanos en los comentarios qué le agregarías a la lista.'),
 ('9','mar 1/12 20.00','Reel de 11 s','R07 Te la llevamos',RE+r'\R07 Te la llevamos\final','R07 portada.png',
  'Te la llevamos a Grand Bourg, San Lorenzo, San Lorenzo Chico, El Tipal y La Almudena. Si estás en otra zona, escribinos y lo vemos.\n\nPedidos al 387 483 4041 o al 387 468 4498.'),
 ('10','mié 2/12 20.00','Carrusel de 4','P13 Achilata en tu fiesta',PU+r'\P13 Achilata en tu fiesta\final','P13 1 en tu fiesta.png',
  'Achilata en tu fiesta. En Tucumán no hay fiesta sin achilata, y ahora en Salta tampoco.\n\nVamos con el carrito, los vasitos, las cucharitas y quien sirve. Casamientos, 15, cumples, empresas y clubes.\n\nPedí tu presupuesto con la fecha y la cantidad de invitados al 387 483 4041 o al 387 468 4498.'),
]
BIO='Helado tucumano en Salta 🍧\nPotes y carrito para eventos\nEnvíos a San Lorenzo, El Tipal, Grand Bourg y más\nPedí al 387 483 4041 o 387 468 4498'

PROX=[
 ('1 encuesta pote.png','jue 26/11, 18.00','Sticker de Encuesta en el hueco del medio: 1 kg o Medio kilo.'),
 ('2 ya probaste.png','vie 27/11, 11.00','Sticker de Quiz o Encuesta: Sí, Todavía no. O el deslizador con 🩷.'),
 ('3 hace calor.png','vie 27/11, 16.00','Sticker de Preguntas: cuántos grados hay donde estás. O el sticker de temperatura.'),
 ('4 pedidos abiertos.png','sáb 28/11, 10.00','Sticker de Enlace a wa.me/543874834041 con el texto Pedí acá.'),
 ('5 preguntanos.png','dom 29/11, 12.00','Sticker de Preguntas: lo que quieras saber de la achilata.'),
 ('6 finde.png','jue 3/12, 18.00','Sticker de Cuenta regresiva al sábado, o el de Enlace a WhatsApp.'),
]
DEST=[('Menú','portada 1 menu.png',['Menu 1 precios.png','Menu 2 el menu.png']),
      ('Pedidos','portada 2 pedidos.png',['Pedidos 1 numeros.png','Pedidos 2 como pedir.png','Pedidos 3 pago.png']),
      ('Zonas','portada 3 zonas.png',['Zonas 1 envios.png']),
      ('Eventos','portada 4 eventos.png',['Eventos 1 en tu fiesta.png','Eventos 2 presupuesto.png']),
      ('Achilata','portada 5 achilata.png',['Achilata 1 que es.png','Achilata 2 hay gelata.png'])]

def sin_emoji(t): return ''.join(ch for ch in t if ord(ch)<0x2000 or ch in '°')
def br(t): return sin_emoji(t).replace('\n','<br/>')

S=[]
# ---------- portada ----------
S+=[Spacer(1,60*mm),P('Perfil completo',ParagraphStyle('t',parent=H1,fontSize=52,leading=52)),
    P('@achilatasalta',ParagraphStyle('t2',parent=H1,fontSize=30,leading=34,textColor=BOR)),
    P('qué subir, en qué orden y qué cambiar.',ParagraphStyle('n',parent=NO,fontSize=20,leading=24)),Spacer(1,20*mm),
    P('Jueves 26 de noviembre de 2026. Todo lo que dice este PDF ya está hecho y guardado en la carpeta del proyecto: 10 publicaciones nuevas, 3 reels, 5 portadas de destacadas con sus historias y 6 historias para los próximos días.'),
    P('Carpeta: <b>04_Contenido</b>, en Publicaciones, Reels, Destacadas, Historias/Próximas historias y Perfil completo.'),PageBreak()]

# ---------- el modelo ----------
S+=[P('El modelo: Rocambolesc.',H1),
    P('Revisé las casi 30 cuentas de heladerías del análisis de referencias, más las nuevas capturas de Rocambolesc. La que mejor encaja con Achilata es <b>Rocambolesc</b>, la heladería de Jordi Roca en Girona, de El Celler de Can Roca: 203 mil seguidores y uno de los feeds de helado más reconocibles del mundo.'),
    P('Por qué ella y no otra',H2)]+bul([
    '<b>Usa un solo color de fondo liso en toda la grilla,</b> un rosa sin costuras. Nuestro rojo achilata ya se ve rosado en el celular, como en las dos primeras publicaciones. Es el mismo recurso.',
    '<b>El producto es enorme, recortado y con luz pareja,</b> como nuestro estudio rojo.',
    '<b>El nombre va gigante en crema y el producto lo pisa.</b> La palabra y el helado forman una sola imagen.',
    '<b>Intercala macros a sangre,</b> como la sandía de cerca con una frase chica, para que el feed respire.',
    '<b>Destacadas iguales entre sí,</b> con un signo simple sobre un círculo de color.',
    'Van Leeuwen, Salt and Straw y OddFellows hacen cosas parecidas pero cambian de color en cada post. Kuono es la más cercana en espíritu, pero su paleta es verde y crema. Para nosotros, Rocambolesc es la que se copia.'])+[
    P('Qué copiamos, con nuestro manual',H2)]+bul([
    '<b>Fondo:</b> rojo achilata #E7364A liso con grano fino. Sin degradés.',
    '<b>Títulos:</b> Bricolage ExtraBold en crema #FFF3E2, con borde del mismo color para engordarlos. Nunca blanco puro.',
    '<b>Palabra gigante pisada por el producto:</b> 32°, Cómo pedir, No deslices.',
    '<b>Macros a sangre</b> de la textura del helado con la frase encima: Etiquetá y el reel La textura.',
    '<b>Series con plantilla fija:</b> los pasos de Cómo pedir con el número gigante, y el humor de No deslices.',
    '<b>Ink Free</b> solo para la nota chica, como en las piezas aprobadas.',
    '<b>Destacadas:</b> un ícono de línea crema sobre rojo, todas iguales.'])+[
    P('Lo que no copiamos',H2)]+bul(['La tipografía fina de Rocambolesc: la nuestra es Bricolage ExtraBold.','Los colores extra de sus fechas especiales. Nos quedamos con rojo y crema.'])+[PageBreak()]

# ---------- maqueta ----------
S+=[P('Así queda el perfil.',H1),
    P('Doce publicaciones, de la más nueva arriba a la izquierda. Las dos de abajo a la derecha ya están subidas. Cada fila mezcla una pieza de producto, una de tipografía y un macro o un reel, así nunca hay dos iguales juntas.'),
    img(PC+r'\maqueta del perfil.png',96*mm),PageBreak()]

# ---------- perfil ----------
S+=[P('1. Cambios en el perfil, hoy.',H1),
    P('Editar perfil',H2)]+bul([
    '<b>Nombre:</b> Achilata Salta. Hoy dice solo Achilata. Con Salta te encuentran en el buscador.',
    '<b>Foto de perfil:</b> la nueva, <b>Perfil completo/foto de perfil 1080.png</b>. Es el mismo logo rojo sobre blanco pero más grande, porque hoy la bajada no se lee en el círculo chico.',
    '<b>Presentación:</b> reemplazar la actual por esta. Usa 144 de los 150 caracteres y suma los eventos:'])+[
    P(br(BIO),CP),P('La primera línea termina con el emoji de helado 🍧, que el PDF no muestra. Está completo en textos_para_copiar.md.'.replace(' 🍧',''),CH)]+bul([
    '<b>Enlaces:</b> agregar la web <b>achilata-salta.vercel.app</b> con el título Pedí online y eventos, y <b>wa.me/543874834041</b> con el título Pedidos por WhatsApp.',
    '<b>Categoría:</b> Heladería. <b>Botón de contacto:</b> WhatsApp al 387 483 4041.',
    '<b>Descubrir personas:</b> cerrarlo con la cruz, para que el perfil se vea limpio.',
    '<b>Banners:</b> por ahora no hace falta.'])+[
    P('Fijar publicaciones',H2),
    P('Cuando estén subidas, fijar arriba de todo estas tres, en este orden: <b>Cómo pedir</b>, <b>El menú</b> y <b>Achilata en tu fiesta</b>. Son las que responden lo que más preguntan.'),PageBreak()]

# ---------- destacadas ----------
filas=[[P('<b>Destacada</b>',CH),P('<b>Portada</b>',CH),P('<b>Historias, en orden</b>',CH)]]
for n,por,hs in DEST:
    filas.append([P(f'<b>{n}</b>',CH),img(DE+'\\'+por,14*mm),P('<br/>'.join(hs),CH)])
t=Table(filas,colWidths=[30*mm,25*mm,110*mm])
t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LINEBELOW',(0,0),(-1,-1),0.5,ROSA),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
S+=[P('2. Las destacadas.',H1),
    P('Cinco destacadas, en este orden: Menú, Pedidos, Zonas, Eventos y Achilata. Todo está en <b>04_Contenido/Destacadas</b>.'),t,
    P('Cómo armarlas',H2)]+bul([
    'Instagram solo deja destacar historias que ya se subieron. Subí cada historia de la tabla, con unos minutos entre una y otra, y al terminar tocá Destacar.',
    'Para la portada: mantené apretada la destacada, Editar destacada, Editar portada, y elegí de la galería el archivo portada. El ícono queda centrado en el círculo.',
    'Cuando lleguen los primeros mensajes de clientes, sumamos una sexta destacada, Clientes, con capturas reales y su permiso.'])+[PageBreak()]

# ---------- publicaciones ----------
S+=[P('3. Las 10 publicaciones, en orden.',H1),
    P('Una o dos por día, con más fuerza de jueves a domingo. El horario es una base: si un día no se puede, se corre todo un lugar. El orden sí importa, porque arma la grilla de la maqueta.'),
    P('el texto de cada una va listo para copiar y pegar.',NO)]
for num,cuando,fmt,nombre,car,port,cap in PUBS:
    fotos=sorted(f for f in os.listdir(car) if f.endswith(('.png','.mp4')) and 'portada' not in f) if 'R' not in nombre[:1] else sorted(f for f in os.listdir(car) if f.endswith('.mp4'))
    info=[P(f'<b>{num}. {nombre[4:]}</b>',ParagraphStyle('x',parent=H2,spaceBefore=0)),P(f'{cuando} · {fmt}',CH),
          P('Archivos, en orden: '+', '.join(fotos),CH),P(br(cap),CP)]
    tb=Table([[img(car+'\\'+port,32*mm),info]],colWidths=[38*mm,127*mm])
    tb.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')]))
    S.append(KeepTogether([tb,Spacer(1,4*mm)]))
S+=[P('Al subir cada una',H2)]+bul([
    '<b>Carruseles:</b> se suben todas las placas en el orden de los archivos. La 1 es la portada.',
    '<b>Reels:</b> los videos van sin audio a propósito. En Instagram elegí un audio en tendencia, con el volumen bajo. En Portada, Agregar desde la galería, elegí el PNG portada. Dejá activado Mostrar en la cuadrícula de fotos.',
    '<b>Antes de publicar,</b> revisá cómo se ve recortada en la grilla: las piezas ya están pensadas para el recorte 3:4.',
    '<b>Después de publicar,</b> compartila en historias con el sticker de publicación.',
    'Respondé cada comentario y mensaje en la primera hora. Es lo que más empuja el alcance.'])+[PageBreak()]

# ---------- próximas historias ----------
filas=[[P('<b>Historia</b>',CH),P('<b>Cuándo</b>',CH),P('<b>Qué sticker agregar en Instagram</b>',CH)]]
for f,cu,st in PROX:
    filas.append([img(PX+'\\'+f,20*mm),P(cu,CH),P(sin_emoji(st).replace('  ',' '),CH)])
t=Table(filas,colWidths=[28*mm,32*mm,105*mm])
t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LINEBELOW',(0,0),(-1,-1),0.5,ROSA),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
S+=[P('4. Las próximas historias.',H1),
    P('El cronograma de historias queda en pausa, como pediste. Estas seis son interactivas y están hechas con un hueco libre para el sticker. Están en <b>04_Contenido/Historias/Próximas historias</b>.'),t,
    P('Además, cada día',H2)]+bul(['Compartí la publicación del día en historias.','Subí lo real: el pote saliendo del freezer, una entrega o la calle con sol. Con el celular, sin diseño, una o dos por día. Lo real le gana a lo perfecto.'])+[PageBreak()]

# ---------- qué cambiar y qué falta ----------
S+=[P('5. Qué cambiar y qué falta.',H1),
    P('Lo más importante: fotos reales',H2),
    P('Todas las piezas usan las imágenes de producto del 19/11, que no son fotos de nuestro producto. Sirven para arrancar, pero <b>lo que más va a hacer crecer la cuenta es la foto real</b>. En cuanto tengan el producto, sacá estas tomas con el celular, de día, con luz de ventana y sin flash:'),
    ]+bul(['Pote de 1 kg y de medio kilo cerrados, de frente, sobre una mesa lisa y clara.','Pote abierto desde arriba, que se vea la textura.','Cuchara entrando, en foto y en video lento de 5 a 10 segundos.','Sirviendo en una copa de vidrio, en video.','Mano con el pote al sol, en un lugar reconocible de Salta.','Ustedes dos preparando, entregando o probando. Rocambolesc muestra siempre a su gente y es lo que más se comenta.','Clientes probando por primera vez, con su permiso.'])+[
    P('Con esas fotos rehago las piezas en el mismo estudio rojo, y así la grilla sigue igual de pareja.'),
    P('Otros cambios',H2)]+bul([
    '<b>Las dos publicaciones subidas,</b> Hay achilata en Salta y El menú, quedan como están: ya tienen el fondo rojo y los títulos crema.',
    '<b>La destacada Clientes</b> se suma con los primeros mensajes reales.',
    '<b>Precios de eventos:</b> no se publican hasta confirmar el costo del kilo con el proveedor. Por eso Eventos pide presupuesto por WhatsApp.',
    '<b>Turnos de entrega:</b> no se publican hasta que los dos los confirmen.',
    '<b>Después del 2/12</b> armamos la segunda tanda de 9 con el mismo sistema.'])+[
    P('Checklist del día',H2)]+bul(['Cambiar nombre, foto, presentación y enlaces.','Subir las 12 historias de destacadas y armar las 5 destacadas con su portada.','Publicar la 1 y la 2 de la lista.','Subir la historia 1 con la encuesta.','Responder todo en la primera hora.'])

def fondo(c,d):
    c.saveState(); c.setFillColor(CRE); c.rect(0,0,A4[0],A4[1],fill=1,stroke=0)
    c.setFillColor(ROJ); c.setFont('RG',8); c.drawRightString(A4[0]-18*mm,10*mm,f'achilata. · perfil completo · {d.page}'); c.restoreState()
out=PC+r'\Perfil completo Achilata.pdf'
doc=BaseDocTemplate(out,pagesize=A4,leftMargin=22*mm,rightMargin=22*mm,topMargin=20*mm,bottomMargin=18*mm,title='Perfil completo @achilatasalta',author='Achilata Salta')
doc.addPageTemplates([PageTemplate('p',[Frame(doc.leftMargin,doc.bottomMargin,doc.width,doc.height,id='f')],onPage=fondo)])
doc.build(S)

# textos para copiar, con emojis
with open(PC+r'\textos_para_copiar.md','w',encoding='utf8') as f:
    f.write('# Textos para copiar · perfil completo 26/11/2026\n\nSale de `fuente/generar_pdf.py`.\n\n## Presentación\n\n```\n'+BIO+'\n```\n\n')
    for num,cuando,fmt,nombre,car,port,cap in PUBS:
        f.write(f'## {num}. {nombre} · {cuando} · {fmt}\n\n```\n{cap}\n```\n\n')
print(out)
