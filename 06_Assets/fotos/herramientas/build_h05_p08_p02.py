import sys,os,glob
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from estudio2 import *
V=sys.argv[1]; O=sys.argv[2]; os.makedirs(O,exist_ok=True)
S=(1080,1920); P=(1080,1350)

def fit(t,w,fn=XB,mx=400):
    s=mx
    while ancho(t,fn(s))>w: s-=2
    return fn(s)

# ================= H05 1 · envíos · foto 05, la mano que te la alcanza =================
L=Lienzo(*S,seed=21)
# arriba el título, debajo la nota, después la foto y abajo la bajada
TB=500                                  # base del título
G=fit('Envíos.',930)
NB=TB+72                                # base de la nota, con el mismo aire que tenía con el título
sc=1.12; y=NB+58-round(435*sc)          # el helado arranca con ese mismo aire debajo de la nota
F,a=cut(V,'05'); x=1080-round(a.shape[1]*sc)
A=L.poner(F,a,sc,x,y); L.sombra_aire(A,dx=30,dy=46,blur=34,fuerza=0.30)
def atras(d,im):
    T(d,72,TB,'Envíos.',G)
    T(d,80,1560,'Hoy salimos a repartir.',RG(50),stroke=False)
    T(d,82,1614,'Grand Bourg, San Lorenzo Chico, San Lorenzo,',RG(32),stroke=False)
    T(d,82,1656,'El Tipal, La Almudena y más.',RG(32),stroke=False)
def adelante(d,im):
    d.text((1000,NB),'llega bien fría.',font=INK(40),fill=CREMA,anchor='rs')
L.render(atras,adelante,natural=True).save(f'{O}/H05 1 envios.png')

# ================= H05 2 · pedidos · foto 07, pote apoyado con su cuchara =================
L=Lienzo(*S,seed=22)
F,a=cut(V,'07'); sc=1.08; base=1650; y=base-round(1194*sc)
A=L.poner(F,a,sc,0,y); L.sombra_piso(A,base)
def atras(d,im):
    im.alpha_composite(logo(150),(80,250))
    T(d,82,420,'Pedidos por WhatsApp.',RG(50),stroke=False)
    f=fit('387 483 4041',920)
    T(d,78,560,'387 483 4041',f); T(d,78,560+round(f.size*1.0),'387 468 4498',f)
def adelante(d,im):
    d.text((1000,775),'y te la llevamos.',font=INK(54),fill=CREMA,anchor='rs')
L.render(atras,adelante).save(f'{O}/H05 2 pedidos.png')

# ================= P08 · Achilata, sustantivo · carrusel =================
# 1 · la palabra, con la bocha pisándola
L=Lienzo(*P,seed=31)
F,a=cut(V,'10'); sc=0.9; y=415-round(320*sc); x=600-round((107+986)/2*sc)
A=L.poner(F,a,sc,x,y); L.sombra_aire(A,dx=36,dy=40,blur=34,fuerza=0.30)
G=fit('Achilata.',920)
def atras(d,im):
    d.text((80,150),'a·chi·la·ta',font=RG(36),fill=CREMA,anchor='ls')
    d.text((1000,150),'sustantivo femenino.',font=RG(36),fill=CREMA,anchor='rs')
    T(d,74,430,'Achilata.',G)
L.render(atras).save(f'{O}/P08 1 achilata.png')

# 2 · qué es
L=Lienzo(*P,seed=32)
F,a=cut(V,'07'); sc=0.88; base=1230; y=base-round(1194*sc)
A=L.poner(F,a,sc,0,y); L.sombra_piso(A,base)
def atras(d,im):
    f=XB(120); T(d,80,230,'Helado de agua',f); T(d,80,350,'tucumano.',f)
    T(d,82,420,'Fucsia, frío y de cuchara.',RG(40),stroke=False)
L.render(atras).save(f'{O}/P08 2 helado de agua.png')

# 3 · de dónde viene el nombre
L=Lienzo(*P,seed=33)
F,a=cut(V,'14'); sc=0.95; x=0; y=440-round(69*sc)
A=L.poner(F,a,sc,x,y); L.sombra_aire(A,dx=32,dy=42,blur=32,fuerza=0.28)
G=fit('hay gelata.',920)
def atras(d,im):
    T(d,82,190,'Dicen que el nombre viene de',RG(40),stroke=False)
    T(d,74,380,'hay gelata.',G)
def adelante(d,im):
    d.text((1000,480),'gracias, nonos italianos.',font=INK(48),fill=CREMA,anchor='rs')
L.render(atras,adelante).save(f'{O}/P08 3 hay gelata.png')

# 4 · cómo se come
L=Lienzo(*P,seed=34)
F,a=cut(V,'32'); sc=0.84; base=1190; y=base-round(1027*sc)
A=L.poner(F,a,sc,0,y); L.sombra_piso(A,base,largo=0.30,inclina=0.55,fuerza=0.38)
def atras(d,im):
    f=fit('Se come con calor',900,mx=112)
    for i,s in enumerate(['Se come con calor','y en buena','compañía.']): T(d,80,215+i*round(f.size*0.96),s,f)
def adelante(d,im):
    im.alpha_composite(logo(160),(80,1270-logo(160).height))
L.render(atras,adelante).save(f'{O}/P08 4 compania.png')

# ================= P02 El menú · v2, sombras rehechas =================
L=Lienzo(*P,seed=41)
F,a=cut(V,'28'); sc=0.74; base=1200; y=base-round(1280*sc); x=540-round((112+882)/2*sc)
A=L.poner(F,a,sc,x,y); L.sombra_piso(A,base)
def atras(d,im): T(d,80,330,'El menú.',XB(220))
def adelante(d,im):
    d.text((84,398),'corto, como tiene que ser.',font=INK(50),fill=CREMA)
    lg=logo(170); im.alpha_composite(lg,(80,1270-lg.height))
L.render(atras,adelante).save(f'{O}/P02 1 el menu.png')

L=Lienzo(*P,seed=42)
F,a=cut(V,'11'); sc=0.9; y=520-round(131*sc); x=540-round((22+1049)/2*sc)
A=L.poner(F,a,sc,x,y); L.sombra_aire(A,dx=26,dy=30,blur=40,fuerza=0.26)
def atras(d,im):
    T(d,80,250,'1 kg.',XB(200)); T(d,82,370,'$12.000',XB(96))
    T(d,82,440,'Para la mesa entera.',RG(40),stroke=False)
L.render(atras).save(f'{O}/P02 2 un kilo.png')

L=Lienzo(*P,seed=43)
F,a=cut(V,'02'); sc=0.9; x=1080-round(a.shape[1]*sc); y=480-round(129*sc)
A=L.poner(F,a,sc,x,y); L.sombra_aire(A,dx=30,dy=40,blur=32,fuerza=0.28)
def atras(d,im):
    T(d,80,230,'Medio kilo.',XB(150)); T(d,82,345,'$8.000',XB(96))
    T(d,82,415,'Para vos y alguien más.',RG(40),stroke=False)
L.render(atras).save(f'{O}/P02 3 medio kilo.png')

L=Lienzo(*P,seed=44)
F,a=cut(V,'16'); sc=0.62; base=1250; x=1080-round(a.shape[1]*sc); y=base-round(1059*sc)
A=L.poner(F,a,sc,x,y); L.sombra_piso(A,base)
def pill(d,x,y,w,h,text,font):
    d.rounded_rectangle((x,y,x+w,y+h),radius=h//2,fill=CREMA)
    d.text((x+w/2,y+h/2+2),text,font=font,fill=ROJ,anchor='mm')
def atras(d,im):
    T(d,80,200,'Cómo pedir.',XB(130))
    for i,s in enumerate(['Escribinos por WhatsApp.','Elegí tu pote.','Te la llevamos a casa.']):
        T(d,82,290+i*56,s,RG(40),stroke=False)
    pill(d,80,480,450,88,'387 483 4041',XB(44)); pill(d,550,480,450,88,'387 468 4498',XB(44))
    for i,s in enumerate(['Delivery en Grand Bourg, San Lorenzo Chico,','San Lorenzo, El Tipal y La Almudena.','Transferencia o efectivo.']):
        T(d,82,650+i*46,s,RG(32),stroke=False)
def adelante(d,im):
    lg=logo(170); im.alpha_composite(lg,(80,1270-lg.height))
L.render(atras,adelante).save(f'{O}/P02 4 como pedir.png')

# hojas de control
def hoja(pat,w,h,name):
    fs=sorted(glob.glob(f'{O}/{pat}')); s=Image.new('RGB',(len(fs)*(w+10)+10,h+20),'#777')
    for i,p in enumerate(fs): s.paste(Image.open(p).resize((w,h),Image.LANCZOS),(10+i*(w+10),10))
    s.save(f'{O}/../hoja_{name}.jpg',quality=88)
hoja('H05 *.png',540,960,'H05'); hoja('P08 *.png',432,540,'P08'); hoja('P02 *.png',432,540,'P02')
