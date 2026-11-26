# Feed completo 26/11/2026 · portadas de destacadas, historias para destacadas y próximas historias.
# Uso: python build_feed_historias.py <carpeta de recortes V>
from feed_comun import *
import shutil
V=sys.argv[1]; W,H=S
def colocar(L,n,sc,px,py,ref='cb'):
    F,a=cut(V,n)
    ys,xs=np.where(a>0.5); x0,y0,x1,y1=xs.min(),ys.min(),xs.max(),ys.max()
    rx={'c':(x0+x1)/2,'l':x0,'r':x1}[ref[0]]; ry={'b':y1,'t':y0,'c':(y0+y1)/2}[ref[1]]
    return L.poner(F,a,sc,round(px-rx*sc),round(py-ry*sc))
DEST=C+r'\Destacadas'; PROX=C+r'\Historias\Próximas historias'
for d in (DEST,PROX): os.makedirs(d,exist_ok=True)

# ================= portadas de destacadas: ícono de línea crema sobre rojo =================
def icono(nombre,dibujar,seed):
    k=4; R=Image.new('L',(W*k,H*k),0); d=ImageDraw.Draw(R)
    cx,cy=W*k//2,H*k//2; u=k*1.0; lw=round(30*k)
    dibujar(d,cx,cy,u,lw)
    m=np.asarray(R.resize((W,H),Image.LANCZOS)).astype(np.float32)/255
    L=Lienzo(W,H,seed=seed); bg=L.render(None,None)
    b=np.asarray(bg).astype(np.float32); cr=np.array([255,243,226],np.float32)
    out=b*(1-m[...,None])+cr*m[...,None]
    Image.fromarray(np.clip(out,0,255).astype(np.uint8)).save(f'{DEST}\\portada {nombre}.png')
def linea(d,pts,lw): d.line(pts,fill=255,width=lw,joint='curve'); [d.ellipse((x-lw/2,y-lw/2,x+lw/2,y+lw/2),fill=255) for x,y in (pts[0],pts[-1])]
def i_menu(d,cx,cy,u,lw):   # pote con su bocha
    w1,w2,h=230*u,170*u,210*u; top=cy-20*u
    linea(d,[(cx-w1,top),(cx-w2,top+h),(cx+w2,top+h),(cx+w1,top)],lw); linea(d,[(cx-w1-20*u,top),(cx+w1+20*u,top)],lw)
    d.arc((cx-200*u,top-200*u,cx+200*u,top+200*u),180,360,fill=255,width=lw)
def i_pedidos(d,cx,cy,u,lw):   # globo de chat
    d.rounded_rectangle((cx-260*u,cy-200*u,cx+260*u,cy+130*u),radius=120*u,outline=255,width=lw)
    linea(d,[(cx-150*u,cy+120*u),(cx-190*u,cy+230*u),(cx-60*u,cy+128*u)],lw)
    for dx in (-110,0,110): d.ellipse((cx+dx*u-26*u,cy-60*u,cx+dx*u+26*u,cy-8*u),fill=255)
def i_zonas(d,cx,cy,u,lw):   # pin de mapa
    r=170*u; c=cy-90*u
    d.arc((cx-r,c-r,cx+r,c+r),150,30,fill=255,width=lw)
    a1,a2=np.radians(150),np.radians(30)
    linea(d,[(cx+r*np.cos(a1),c+r*np.sin(a1)),(cx,cy+250*u),(cx+r*np.cos(a2),c+r*np.sin(a2))],lw)
    d.ellipse((cx-62*u,c-62*u,cx+62*u,c+62*u),outline=255,width=lw)
def i_eventos(d,cx,cy,u,lw):   # estrella de fiesta
    pts=[]
    for i in range(11):
        a=np.radians(-90+i*36); r=(250 if i%2==0 else 110)*u
        pts.append((cx+r*np.cos(a),cy+20*u+r*np.sin(a)))
    linea(d,pts,lw)
def i_achilata(d,cx,cy,u,lw):   # cuchara
    d.ellipse((cx-110*u,cy-260*u,cx+110*u,cy-10*u),outline=255,width=lw)
    linea(d,[(cx,cy-10*u),(cx,cy+270*u)],lw)
for n,f,s in [('1 menu',i_menu,601),('2 pedidos',i_pedidos,602),('3 zonas',i_zonas,603),('4 eventos',i_eventos,604),('5 achilata',i_achilata,605)]:
    icono(n,f,s)

# ================= historias, estilo H05 1 aprobado =================
def historia(ruta,titulo,nota,n,sc,px,py,ref,sombra,lineas,seed,pills=False,hueco=None):
    tl=titulo if isinstance(titulo,list) else [titulo]
    G=fit(max(tl,key=lambda t:ancho(t,XB(100))),930,mx=260); g=round(G.size*0.92)
    TB=300+round(G.size*0.72)
    # el producto arranca con aire debajo de la nota y nunca pisa el título
    tope=TB+(len(tl)-1)*g+150
    F_,a_=cut(V,n); ys,xs=np.where(a_>0.5); alto=ys.max()-ys.min()
    if ref[1]=='b' and py-alto*sc<tope: sc=(py-tope)/alto
    L=Lienzo(W,H,seed=seed); A=colocar(L,n,sc,px,py,ref)
    if sombra=='piso': L.sombra_piso(A,py)
    elif sombra=='aire': L.sombra_aire(A,dx=30,dy=46,blur=34,fuerza=0.30)
    def atras(d,im):
        for i,t in enumerate(tl): T(d,72,TB+i*g,t,G)
    def adelante(d,im):
        last=TB+(len(tl)-1)*g
        if nota: d.text((1000,last+72),nota,font=INK(44),fill=CREMA,anchor='rs')
        y=1670-len(lineas)*46-(90 if pills else 0)
        for i,t in enumerate(lineas):
            T(d,80,y+i*46 if i else y,t,RG(50) if i==0 else RG(34),stroke=False)
            if i==0: y+=12
        if pills: numeros(d,80,1670-70)
    L.render(atras,adelante).save(ruta)

# destacada Pedidos
historia(f'{DEST}\\Pedidos 2 como pedir.png',['Cómo pedir.'],'en cuatro pasos.','16',0.80,1080,1330,'rb','piso',
         ['Escribinos, elegí tu pote,','pasanos tu zona y pagá con','transferencia o efectivo.'],611,pills=True)
historia(f'{DEST}\\Pedidos 3 pago.png',['Pagás como','quieras.'],'y te la llevamos.','07',0.95,0,1400,'lb','piso',
         ['Transferencia o efectivo.','El alias te lo pasamos por el chat','cuando confirmamos tu pedido.'],612)
# destacada Eventos
historia(f'{DEST}\\Eventos 1 en tu fiesta.png',['Achilata en','tu fiesta.'],'nuevo en Salta.','32',0.84,0,1420,'lb','piso',
         ['Vamos con el carrito.','Casamientos, 15, cumples, empresas y clubes.','Vasitos, cucharitas y quien sirve.'],613)
historia(f'{DEST}\\Eventos 2 presupuesto.png',['Pedí tu','presupuesto.'],'con la fecha y los invitados.','05',0.95,1080,1400,'rb','aire',
         ['Escribinos y te lo armamos.'],614,pills=True)
# destacada Achilata
historia(f'{DEST}\\Achilata 1 que es.png',['Achilata.'],'sustantivo femenino.','01',0.90,540,1470,'cb','piso',
         ['Helado de agua tucumano.','Fucsia, frío y de cuchara.'],615)
historia(f'{DEST}\\Achilata 2 hay gelata.png',['hay gelata.'],'gracias, nonos italianos.','28',0.85,540,1420,'cb','piso',
         ['Dicen que el nombre viene de ahí:','los heladeros italianos gritaban hay gelata','y de tanto escucharlo quedó achilata.'],616)

# las que ya estaban hechas y van a destacadas
YA={'Menu 1 precios.png':r'Historias\Día 01 jue 19 nov\final\H01 3 precios 20.30.png',
    'Pedidos 1 numeros.png':r'Historias\Día 05 lun 23 nov\final\H05 2 pedidos.png',
    'Zonas 1 envios.png':r'Historias\Día 05 lun 23 nov\final\H05 1 envios.png'}
for k,v in YA.items(): shutil.copy(f'{C}\\{v}',f'{DEST}\\{k}')
historia(f'{DEST}\\Menu 2 el menu.png',['El menú.'],'corto, como tiene que ser.','28',0.95,540,1450,'cb','piso',
         ['1 kg a $12.000.','Medio kilo a $8.000.','Sabor clásico, el de siempre.'],617)

# ================= próximas historias =================
historia(f'{PROX}\\1 encuesta pote.png',['¿1 kg o','medio kilo?'],'votá acá abajo.','01',0.70,540,1620,'cb','piso',[],621)
historia(f'{PROX}\\2 ya probaste.png',['¿Ya probaste','achilata?'],'contanos con el emoji.','13',0.80,1080,1920,'rb','',[],622)
historia(f'{PROX}\\3 hace calor.png',['Hace calor','en Salta.'],'y se derrite todo.','08',0.80,540,1450,'cb','piso',
         ['¿Cuántos grados hay donde estás?'],623)
historia(f'{PROX}\\4 pedidos abiertos.png',['Pedidos','abiertos.'],'hoy salimos a repartir.','05',1.0,1080,1380,'rb','aire',
         ['Escribinos y te la llevamos.'],624,pills=True)
historia(f'{PROX}\\5 preguntanos.png',['Preguntanos','lo que quieras.'],'respondemos todo.','16',0.75,1080,1620,'rb','piso',[],625)
historia(f'{PROX}\\6 finde.png',['Finde de','achilata.'],'pedila con tiempo.','11',0.85,540,1920+10,'cb','',[],626)

hoja(sorted(glob.glob(DEST+'/portada*.png')),sys.argv[2]+'/hoja_portadas.jpg',w=216,h=384)
hoja(sorted(p for p in glob.glob(DEST+'/*.png') if 'portada' not in p),sys.argv[2]+'/hoja_dest.jpg',w=216,h=384)
hoja(sorted(glob.glob(PROX+'/*.png')),sys.argv[2]+'/hoja_prox.jpg',w=216,h=384)
print('ok')
