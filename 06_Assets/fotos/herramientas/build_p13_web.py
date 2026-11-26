# P13 Pedí desde la web, carrusel de 4, y las historias H24 a H26 de la web · 26/11/2026
# Rehechas a partir de la P17 y las H06 del colega. Reglas nuevas de Lauti:
#  - bordes del recorte difuminados y suaves, con sombra natural: Lienzo.suave = 1.8
#  - el texto nunca pisa el producto: primero se mide dónde termina el texto y el producto va debajo, con aire
#  - textos breves; un solo peso por renglón, también dentro de la tabla de turnos
# Uso: python build_p13_web.py <carpeta de recortes V>
from feed_comun import *
V=sys.argv[1]
SUAVE=1.8; AIRE=70
TURNOS=[('Mediodía','12.00 a 14.00','Domingo','pedí hasta las 10.00'),
        ('Tarde','15.30 a 18.00','Jueves a domingo','pedí hasta las 13.30'),
        ('Noche','19.30 a 21.30','Jueves a domingo','pedí hasta las 18.00'),
        ('Un turno','17.00 a 20.00','Lunes a miércoles','pedí hasta las 15.00')]

def caja(n):
    F,a=cut(V,n); ys,xs=np.where(a>0.5); return F,a,(xs.min(),ys.min(),xs.max(),ys.max())
def producto(L,n,tope,sc,x,borde,sombra='aire',piso=None):
    """pone el producto con su borde de arriba en tope. borde: 'r' pegado a la derecha, 'c' centrado, 'l' a la izquierda.
    Si el recorte toca un borde de la foto original, sale del cuadro por ese mismo borde."""
    F,a,(x0,y0,x1,y1)=caja(n)
    px={'r':L.W-x1*sc if x1>a.shape[1]-4 else x-x1*sc,'c':x-(x0+x1)/2*sc,'l':-x0*sc if x0<3 else x-x0*sc}[borde]
    A=L.poner(F,a,sc,round(px),round(tope-y0*sc))
    if sombra=='aire': L.sombra_aire(A,dx=28,dy=40,blur=38,fuerza=0.26)
    elif sombra=='piso': L.sombra_piso(A,piso)
    return A
def tabla(d,x,y,w,h,gap,f1,f2):
    for i,(n,hs,dias,cierre) in enumerate(TURNOS):
        t=y+i*(h+gap); d.rounded_rectangle((x,t,x+w,t+h),radius=round(h*0.3),fill=CREMA)
        a=t+round(h*0.46); b=t+round(h*0.80)
        d.text((x+28,a),n,font=f1,fill=ROJ,anchor='ls'); d.text((x+w-28,a),hs,font=f1,fill=ROJ,anchor='rs')
        d.text((x+28,b),dias,font=f2,fill=ROJ,anchor='ls'); d.text((x+w-28,b),cierre,font=f2,fill=ROJ,anchor='rs')
    return y+4*h+3*gap
def lienzo(W,H,seed):
    L=Lienzo(W,H,seed=seed); L.suave=SUAVE; return L

OP=f'{C}\\Publicaciones\\P13 Pedí desde la web\\final'; os.makedirs(OP,exist_ok=True)
OH=f'{C}\\Historias'
hechos=[]
def guardar(img,ruta): img.save(ruta); hechos.append(ruta)

# ---------------- P13 1 · Pedí desde la web ----------------
L=lienzo(*P,1301)
G=fit('Pedí desde la web.',930,mx=150)
tb=150+round(G.size*0.72)          # base del título
fin_texto=tb+62                     # nota de abajo
A=producto(L,'05',fin_texto+AIRE,1.0,0,'r')
def at(d,im):
    T(d,72,tb,'Pedí desde la web.',G)
def ad(d,im):
    d.text((1000,tb+62),'potes, día y turno.',font=INK(46),fill=CREMA,anchor='rs')
    poner_logo(im,80,1275,150)
guardar(L.render(at,ad),f'{OP}\\P13 1 pedi desde la web.png')

# ---------------- P13 2 · Elegí tus potes ----------------
L=lienzo(*P,1302)
G=fit('Elegí tus potes.',930,mx=150); f=XB(84)
tb=150+round(G.size*0.72); r1=tb+120; r2=r1+96
t22=r2+AIRE; A=producto(L,'22',t22,max(0.92,(P[1]+40-t22)/815),540,'c',sombra='')   # el borde cortado del pote sale por abajo
def at(d,im):
    T(d,72,tb,'Elegí tus potes.',G)
    T(d,76,r1,'1 kg',f); T(d,1004,r1,'$12.000',f,anchor='rs')
    T(d,76,r2,'Medio kilo',f); T(d,1004,r2,'$8.000',f,anchor='rs')
guardar(L.render(at,None),f'{OP}\\P13 2 elegi tus potes.png')

# ---------------- P13 3 · Elegí tu turno ----------------
L=lienzo(*P,1303)
G=fit('Elegí tu turno.',930,mx=150)
tb=150+round(G.size*0.72)
ty=tb+40; fin=ty+4*92+3*14; nota=fin+50
A=producto(L,'13',nota+AIRE,0.62,0,'r',sombra='')
def at(d,im):
    T(d,72,tb,'Elegí tu turno.',G)
def ad(d,im):
    tabla(d,76,ty,928,92,14,XB(32),RG(24))
    T(d,80,nota,'Cada turno cierra unas horas antes.',RG(32),stroke=False)
guardar(L.render(at,ad),f'{OP}\\P13 3 elegi tu turno.png')

# ---------------- P13 4 · Pagás como quieras ----------------
L=lienzo(*P,1304)
G=fit('Pagás como quieras.',930,mx=150)
tb=150+round(G.size*0.72); l1=tb+62; l2=l1+46; lk=l2+96
A=producto(L,'02',lk+AIRE,0.62,0,'r',sombra='')
def at(d,im):
    T(d,72,tb,'Pagás como quieras.',G)
    T(d,80,l1,'Transferencia o efectivo.',RG(40),stroke=False)
    T(d,80,l2,'El alias te lo pasamos por WhatsApp.',RG(40),stroke=False)
    T(d,76,lk,'Link en la bio.',XB(76))
guardar(L.render(at,None),f'{OP}\\P13 4 pagas como quieras.png')

# ---------------- historias ----------------
# H24 · Tenemos web
L=lienzo(*S,2401)
G=fit('Tenemos web.',930,mx=230)
tb=300+round(G.size*0.72); l1=tb+70; lk=l1+92
A=producto(L,'05',lk+AIRE+30,1.32,0,'r')
def at(d,im):
    T(d,72,tb,'Tenemos web.',G)
    T(d,80,l1,'Pedí con turno de entrega.',RG(48),stroke=False)
    T(d,76,lk,'Link en la bio.',XB(80))
guardar(L.render(at,None),f'{OH}\\H24 tenemos web.png')

# H25 · Los turnos
L=lienzo(*S,2501)
G=fit('Los turnos.',930,mx=230)
tb=300+round(G.size*0.72); ty=tb+50; fin=ty+4*124+3*18; nota=fin+60
A=producto(L,'16',nota+AIRE+20,0.66,1080,'r',sombra='piso',piso=1680)
def at(d,im):
    T(d,72,tb,'Los turnos.',G)
def ad(d,im):
    tabla(d,76,ty,928,124,18,XB(42),RG(30))
    T(d,80,nota,'Elegís el día y el turno en la web.',RG(40),stroke=False)
guardar(L.render(at,ad),f'{OH}\\H25 los turnos.png')

# H26 · Cómo pedir: tres pasos cortos y el pote debajo, sin tocar el texto
L=lienzo(*S,2601)
G=fit('Cómo pedir.',930,mx=230)
tb=300+round(G.size*0.72)
pasos=['1. Entrá al link de la bio.','2. Elegí potes y turno.','3. Pagá como quieras.']
ys=[tb+80+i*62 for i in range(3)]; yl=ys[-1]+100
A=producto(L,'11',yl+AIRE+20,0.80,540,'c',sombra='')
def at(d,im):
    T(d,72,tb,'Cómo pedir.',G)
    for y,t in zip(ys,pasos): T(d,80,y,t,RG(46),stroke=False)
    T(d,76,yl,'Y te la llevamos.',XB(76))
guardar(L.render(at,None),f'{OH}\\H26 como pedir web.png')

if len(sys.argv)>2:
    hoja(hechos[:4],sys.argv[2]+'/p13.jpg',w=432,h=540)
    hoja(hechos[4:],sys.argv[2]+'/h24.jpg',w=360,h=640)
print('ok')
