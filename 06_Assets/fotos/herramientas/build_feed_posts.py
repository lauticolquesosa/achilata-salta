# Feed completo 26/11/2026 · publicaciones P05, P06, P08, P09, P10 y P12.
# Uso: python build_feed_posts.py <carpeta de recortes V>
from feed_comun import *
V=sys.argv[1]
BB={}
def ct(n):
    F,a=cut(V,n)
    if n not in BB:
        ys,xs=np.where(a>0.5); BB[n]=(xs.min(),ys.min(),xs.max(),ys.max())
    return F,a,BB[n]
def colocar(L,n,sc,px,py,ref='cb'):
    """ubica el recorte por un punto de su caja: cb centro abajo, ct centro arriba, rb, lb, cc"""
    F,a,(x0,y0,x1,y1)=ct(n)
    rx={'c':(x0+x1)/2,'l':x0,'r':x1}[ref[0]]; ry={'b':y1,'t':y0,'c':(y0+y1)/2}[ref[1]]
    return L.poner(F,a,sc,round(px-rx*sc),round(py-ry*sc))
def out(carp,nombre):
    d=f'{C}\\Publicaciones\\{carp}\\final'; os.makedirs(d,exist_ok=True); return f'{d}\\{nombre}.png'
hechos={}
def guardar(img,carp,nombre):
    p=out(carp,nombre); img.save(p); hechos.setdefault(carp,[]).append(p)

# =============== P05 · Hace 32 grados · placa única ===============
K='P05 Hace 32 grados'
L=Lienzo(*P,seed=401)
A=colocar(L,'28',0.64,560,1225); L.sombra_piso(A,1225)
G=XB(580)
def atras(d,im):
    T(d,82,170,'Salta, cuatro de la tarde.',RG(42),stroke=False)
    T(d,540,790,'32°',G,anchor='ms')
def adelante(d,im):
    d.text((1000,236),'y vos sin achilata.',font=INK(46),fill=CREMA,anchor='rs')
    poner_logo(im,80,1275,150)
guardar(L.render(atras,adelante),K,'P05 1 hace 32')

# =============== P06 · Cómo pedir · carrusel de 6 ===============
K='P06 Cómo pedir'
L=Lienzo(*P,seed=901)
A=colocar(L,'05',0.80,1080,280,'rt'); L.sombra_aire(A,dx=30,dy=44,blur=34,fuerza=0.30)
G=fit('pedir.',930)
def atras(d,im):
    T(d,82,170,'Guardalo para el finde.',RG(42),stroke=False)
    T(d,70,1010,'Cómo',G); T(d,70,1010+round(G.size*0.86),'pedir.',G)
def adelante(d,im):
    d.text((1000,236),'en cuatro pasos.',font=INK(46),fill=CREMA,anchor='rs')
guardar(L.render(atras,adelante),K,'P06 1 portada')

def paso(num,titulo,lineas,n,sc,px,py,ref,sombra,seed,extra=None):
    L=Lienzo(*P,seed=seed)
    A=colocar(L,n,sc,px,py,ref)
    if sombra=='piso': L.sombra_piso(A,py)
    else: L.sombra_aire(A,dx=30,dy=42,blur=32,fuerza=0.28)
    def atras(d,im):
        T(d,40,760,num,XB(820))
    def adelante(d,im):
        f=fit(titulo,920,mx=110)
        T(d,80,1010,titulo,f)
        for i,s in enumerate(lineas): T(d,82,1085+i*52,s,RG(40),stroke=False)
        if extra: extra(d,im)
        d.text((1000,110),f'paso {num} de 4',font=INK(40),fill=CREMA,anchor='rs')
    return L.render(atras,adelante)
guardar(paso('1','Escribinos.',['Por WhatsApp, a cualquiera de los dos.'],'08',0.56,780,880,'cb','piso',902,
              extra=lambda d,im:numeros(d,80,1150)),K,'P06 2 escribinos')
guardar(paso('2','Elegí tu pote.',['1 kg a $12.000.','Medio kilo a $8.000.'],'28',0.62,800,900,'cb','piso',903),K,'P06 3 elegi tu pote')
guardar(paso('3','Pasanos tu zona.',['Grand Bourg, San Lorenzo Chico, San Lorenzo,','El Tipal y La Almudena. Otras, consultanos.'],'05',0.66,1080,860,'rb','aire',904),K,'P06 4 tu zona')
guardar(paso('4','Pagá como quieras.',['Transferencia o efectivo.'],'16',0.58,1080,860,'rb','piso',905),K,'P06 5 paga')

L=Lienzo(*P,seed=906)
A=colocar(L,'28',0.60,700,1150,'cb'); L.sombra_piso(A,1150)
G=fit('Y te la llevamos',930,mx=200)
def atras(d,im):
    T(d,72,250,'Y te la llevamos',G)
    F2=fit('fría.',520); T(d,72,250+round(F2.size*0.92),'fría.',F2)
def adelante(d,im):
    numeros(d,80,1196,h=62,w=300)
    poner_logo(im,1000-150,1258,150)
guardar(L.render(atras,adelante),K,'P06 6 te la llevamos')

# =============== P08 · Etiquetá · placa única sobre la textura ===============
K='P08 Etiquetá a quien le debés'
im=macro('04',1080,1350,0.5,0.0,1.0,oscurecer=0.08,seed=1101)
d=ImageDraw.Draw(im)
f=fit('le debés una',860,mx=128)
for i,s in enumerate(['Etiquetá','a quien','le debés una','achilata.']): T(d,80,850+i*round(f.size*0.90),s,f)
d.text((1000,1270),'y que pague esta vez.',font=INK(46),fill=CREMA,anchor='rs')
guardar(im.convert('RGB'),K,'P08 1 etiqueta')

# =============== P09 · No deslices · carrusel de 5 ===============
K='P09 No deslices'
L=Lienzo(*P,seed=501)
A=colocar(L,'22',1.0,540,1350+60,'cb')
G=fit('deslices.',930)
def atras(d,im):
    T(d,70,420,'No',G); T(d,70,420+round(G.size*0.86),'deslices.',G)
guardar(L.render(atras,None),K,'P09 1 no deslices')

L=Lienzo(*P,seed=502)
A=colocar(L,'16',0.55,1080,1180,'rb'); L.sombra_piso(A,1150,fuerza=0.34)
G=fit('En serio.',930)
def atras(d,im): T(d,70,520,'En serio.',G)
def adelante(d,im): d.text((1000,610),'te va a dar antojo.',font=INK(50),fill=CREMA,anchor='rs')
guardar(L.render(atras,adelante),K,'P09 2 en serio')

L=Lienzo(*P,seed=503)
A=colocar(L,'08',0.95,540,1350+330,'cb')
G=fit('Último',930)
def atras(d,im):
    T(d,70,400,'Último',G); T(d,70,400+round(G.size*0.86),'aviso.',G)
guardar(L.render(atras,None),K,'P09 3 ultimo aviso')

L=Lienzo(*P,seed=504)
A=colocar(L,'11',0.74,540,1350+10,'cb')
G=fit('Bueno, vos te',930,mx=150)
def atras(d,im):
    for i,s in enumerate(['Bueno, vos te','lo buscaste.']): T(d,74,230+i*round(G.size*0.92),s,G)
guardar(L.render(atras,None),K,'P09 4 te lo buscaste')

L=Lienzo(*P,seed=505)
A=colocar(L,'05',0.92,1080,1240,'rb'); L.sombra_aire(A,dx=30,dy=44,blur=34,fuerza=0.30)
G=fit('Pedí la tuya.',930,mx=170)
def atras(d,im):
    T(d,74,260,'Pedí la tuya.',G)
    T(d,82,340,'1 kg a $12.000 y medio kilo a $8.000.',RG(40),stroke=False)
def adelante(d,im):
    numeros(d,80,400)
    poner_logo(im,80,1275,150)
guardar(L.render(atras,adelante),K,'P09 5 pedi la tuya')

# =============== P10 · La achilata anotada · placa única ===============
K='P10 La achilata anotada'
L=Lienzo(*P,seed=1001)
A=colocar(L,'28',0.70,540,1150,'cb'); L.sombra_piso(A,1150)
G=fit('La achilata,',920,mx=150)
notas=[ # texto, punto de la nota, punto del producto, alineación
    ('hielo raspado',(110,470),(400,560),'ls'),
    ('receta tucumana',(980,450),(700,540),'rs'),
    ('sabor clásico',(90,760),(330,700),'ls'),
    ('pote de 1 kg',(990,800),(800,860),'rs'),
    ('llega fría a tu casa',(1000,1260),(700,1175),'rs'),
]
def atras(d,im):
    T(d,76,200,'La achilata,',G); T(d,76,200+round(G.size*0.92),'anotada.',G)
def adelante(d,im):
    for t,(tx,ty),(px,py),an in notas:
        d.text((tx,ty),t,font=INK(44),fill=CREMA,anchor=an)
        w=ancho(t,INK(44)); sx=tx+w+12 if an=='ls' else tx-w-12
        d.line([(sx,ty-14),(px,py)],fill=CREMA,width=3)
        d.ellipse((px-7,py-7,px+7,py+7),fill=CREMA)
guardar(L.render(atras,adelante),K,'P10 1 anotada')

# =============== P12 · Achilata en tu fiesta · carrusel de 4 ===============
K='P12 Achilata en tu fiesta'
L=Lienzo(*P,seed=1301)
A=colocar(L,'32',0.86,0,1200,'lb'); L.sombra_piso(A,1200,largo=0.30,inclina=0.55,fuerza=0.38)
G=fit('Achilata en',930,mx=200)
def atras(d,im):
    T(d,82,150,'Nuevo, para eventos en Salta.',RG(42),stroke=False)
    for i,s in enumerate(['Achilata en','tu fiesta.']): T(d,72,370+i*round(G.size*0.92),s,G)
def adelante(d,im): poner_logo(im,1000-150,1275,150)
guardar(L.render(atras,adelante),K,'P12 1 en tu fiesta')

L=Lienzo(*P,seed=1302)
A=colocar(L,'28',0.80,600,1240,'cb'); L.sombra_piso(A,1240)
f=fit('no hay fiesta sin',920,mx=130)
def atras(d,im):
    for i,s in enumerate(['En Tucumán','no hay fiesta sin','achilata.']): T(d,78,220+i*round(f.size*0.94),s,f)
def adelante(d,im): d.text((1000,520),'ahora tampoco en Salta.',font=INK(46),fill=CREMA,anchor='rs')
guardar(L.render(atras,adelante),K,'P12 2 en tucuman')

L=Lienzo(*P,seed=1303)
A=colocar(L,'10',0.78,700,1350+40,'cb')
f=XB(104)
def atras(d,im):
    for i,s in enumerate(['Vamos con','el carrito.']): T(d,80,230+i*100,s,f)
    for i,s in enumerate(['Vasitos, cucharitas y quien sirve.','Casamientos, 15, cumples,','empresas y clubes.']):
        T(d,82,420+i*52,s,RG(40),stroke=False)
guardar(L.render(atras,None),K,'P12 3 el carrito')

L=Lienzo(*P,seed=1304)
A=colocar(L,'13',0.50,1080,1350+150,'rb')
G=fit('Pedí tu',600,mx=200)
def atras(d,im):
    T(d,74,300,'Pedí tu',G); T(d,74,300+round(G.size*0.9),'presupuesto.',fit('presupuesto.',930))
def adelante(d,im):
    T(d,82,560,'Escribinos con la fecha y los invitados.',RG(40),stroke=False)
    numeros(d,80,610)
    T(d,82,750,'Todo el detalle en el link de la bio.',RG(36),stroke=False)
guardar(L.render(atras,adelante),K,'P12 4 presupuesto')

S_=sys.argv[2] if len(sys.argv)>2 else None
if S_:
    for k,v in hechos.items(): hoja(v,f'{S_}/hoja_{k[:3]}.jpg',w=324,h=405)
print('ok')
