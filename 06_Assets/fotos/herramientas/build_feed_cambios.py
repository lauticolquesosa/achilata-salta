# Cambios del 26/11/2026 · Lauti marcó 4 piezas porque la grilla saturaba de rojo.
# Dos con fondo realista de la foto: R07 Te la llevamos y R01 Una cucharada, sobre cielo.
# Dos en blanco puro con la letra en rojo achilata, jugando tipografía y producto: P11 Etiquetá y R03 La textura.
# Uso: python build_feed_cambios.py <carpeta de recortes V>
from feed_comun import *
import estudio2 as E
from extend import extend
import subprocess
V=sys.argv[1]; FPS=30; W,H=S
BLANCO=np.array([255,255,255],np.float32)

# ---------- estudio blanco: mismo método del estudio rojo, con sombra gris cálida ----------
class LienzoB(Lienzo):
    def __init__(s,W_,H_,seed=3):
        super().__init__(W_,H_,seed)
        g=cv2.GaussianBlur(np.random.default_rng(seed).normal(0,1,(H_,W_)).astype(np.float32),(0,0),0.7); g/=g.std()
        s.bg=np.zeros((H_,W_,3),np.float32)+252+g[...,None]*1.4
    def render(s,atras=None,adelante=None,natural=True):
        viejo=(E.RO,E.SOMBRA)
        E.RO=BLANCO; E.SOMBRA=np.array([88,80,78],np.float32)   # sombra gris cálida, sin rebote rojo
        try: return super().render(atras,adelante,natural)
        finally: E.RO,E.SOMBRA=viejo
def colocar(L,n,sc,px,py,ref='cb'):
    F,a=cut(V,n); ys,xs=np.where(a>0.5); x0,y0,x1,y1=xs.min(),ys.min(),xs.max(),ys.max()
    rx={'c':(x0+x1)/2,'l':x0,'r':x1}[ref[0]]; ry={'b':y1,'t':y0,'c':(y0+y1)/2}[ref[1]]
    return L.poner(F,a,sc,round(px-rx*sc),round(py-ry*sc))
def TR(d,x,y,t,f,anchor='ls'): T(d,x,y,t,f,anchor=anchor,fill=ROJ)

# ================= P11 · Etiquetá · blanco puro =================
K='P11 Etiquetá a quien le debés'
L=LienzoB(*P,seed=1111)
A=colocar(L,'22',0.84,540,1250,'cb'); L.sombra_aire(A,dx=26,dy=30,blur=38,fuerza=0.22)
G1=fit('le debés',950); G2=fit('una achilata.',950)
def atras(d,im):
    TR(d,1000,200,'Etiquetá a quien',XB(96),'rs')
    TR(d,62,600,'le debés',G1)
def adelante(d,im):
    TR(d,58,1272,'una achilata.',G2)
    d.text((1000,268),'y que pague esta vez.',font=INK(46),fill=ROJ,anchor='rs')
d0=f'{C}\\Publicaciones\\{K}\\final'; os.makedirs(d0,exist_ok=True)
L.render(atras,adelante).save(f'{d0}\\P11 1 etiqueta.png')

# ---------- video ----------
ease=lambda t:1-(1-min(max(t,0),1))**3
def zoom(img,z,cx=0.5,cy=0.5):
    if abs(z-1)<1e-3: return img.copy()
    cw,ch=W/z,H/z; x0=(W-cw)*cx; y0=(H-ch)*cy
    return img.resize((W,H),Image.BICUBIC,box=(x0,y0,x0+cw,y0+ch))
def capa(items,t,col=CREMA):
    """texto que entra subiendo y apareciendo; devuelve una capa RGBA"""
    lay=Image.new('RGBA',(W,H),(0,0,0,0))
    for t0,x,y,s,f,an,kind in items:
        if t<t0: continue
        k=ease((t-t0)/0.3); l=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(l); dy=round(36*(1-k))
        if kind=='pills':
            fill,txt=(CREMA,ROJ) if col==CREMA else (ROJ,CREMA)
            pill(d,x,y+dy,330,66,'387 483 4041',XB(32),fill,txt); pill(d,x+346,y+dy,330,66,'387 468 4498',XB(32),fill,txt)
        elif kind=='logo':
            lg=logo(f,'crema' if col==CREMA else 'rojo'); l.alpha_composite(lg,(round(x-lg.width/2),round(y-lg.height)+dy))
        elif kind=='ink': d.text((x,y+dy),s,font=f,fill=col,anchor=an)
        else: T(d,x,y+dy,s,f,anchor=an,fill=col)
        if k<1: l.putalpha(l.getchannel('A').point(lambda v:int(v*k)))
        lay.alpha_composite(l)
    return lay
def frame(base,items,t,col=CREMA,mask=None):
    """mask: zona del producto que queda delante del texto"""
    fr=base.copy(); lay=capa(items,t,col)
    if mask is not None:
        a=np.asarray(lay.getchannel('A')).astype(np.float32)*(1-mask); lay.putalpha(Image.fromarray(a.astype(np.uint8)))
    fr.paste(lay,(0,0),lay); return fr
def codificar(escenas,salida):
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',salida],stdin=subprocess.PIPE)
    for dur,fn in escenas:
        for i in range(round(dur*FPS)): p.stdin.write(np.asarray(fn(i/FPS).convert('RGB')).tobytes())
    p.stdin.close(); p.wait()

# ---------- fondo realista: la foto con su cielo extendido hacia arriba ----------
def cielo(n,grain=2.0):
    I=orig(n); h,w=I.shape[:2]; I=cv2.resize(I,(W,round(h*W/w)),interpolation=cv2.INTER_LANCZOS4)
    T_=H-I.shape[0]
    hsv=cv2.cvtColor(np.clip(I,0,255).astype(np.uint8),cv2.COLOR_RGB2HSV)
    sky=(hsv[...,0]>95)&(hsv[...,0]<125)&(hsv[...,1]>60)
    ex=cv2.dilate((~sky).astype(np.uint8),np.ones((25,25),np.uint8))>0
    out=extend(I,ex,0,T_,0,grain=grain).astype(np.float32)
    out=(out-128)*1.04+128
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))

# ================= R07 · Te la llevamos · el helado sobre el edificio, cielo salteño =================
dR=f'{C}\\Reels\\R07 Te la llevamos\\final'; os.makedirs(dR,exist_ok=True)
B09=cielo('09')
zonas=[['Grand Bourg.'],['San Lorenzo.'],['San Lorenzo','Chico.'],['El Tipal.'],['La Almudena.']]
FZ=fit('San Lorenzo.',920,mx=230)
def lineas(ls,t0,y=560): return [(t0,78,y+j*round(FZ.size*0.92),l,FZ,'ls','t') for j,l in enumerate(ls)]
def zona(i):
    return lambda t:frame(zoom(B09,1.0+0.01*(i+t/1.3),0.5,0.9),[(-1,82,380,'Te la llevamos a',RG(52),'ls','t')]+lineas(zonas[i],0.0),t)
def otra(t): return frame(zoom(B09,1.06,0.5,0.9),[(-1,82,380,'Y si estás en otra zona,',RG(52),'ls','t')]+lineas(['consultanos.'],0.0),t)
def fin07(t): return frame(zoom(B09,1.07,0.5,0.9),[(0,78,560,'Pedí la tuya.',FZ,'ls','t'),(0.25,82,650,'1 kg a $12.000 y medio kilo a $8.000.',RG(42),'ls','t'),
                                                   (0.5,80,710,None,None,None,'pills'),(0.8,1000,880,'antes de que se derrita.',INK(54),'rs','ink')],t)
codificar([(1.6,zona(0))]+[(1.3,zona(i)) for i in range(1,5)]+[(1.8,otra),(3.0,fin07)],f'{dR}\\R07 te la llevamos.mp4')
G=fit('Te la llevamos',930,mx=260)
frame(B09,[(-1,72,560,'Te la llevamos',G,'ls','t'),(-1,1000,560+110,'antes de que se derrita.',INK(54),'rs','ink')],1).save(f'{dR}\\R07 portada.png')

# ================= R01 · Una cucharada · la cuchara de madera contra el cielo =================
dR=f'{C}\\Reels\\R01 El ritual\\final'; os.makedirs(dR,exist_ok=True)
B21=cielo('21')
f=fit('Una cucharada',920,mx=170); g=round(f.size*0.95)
L1=(0.2,80,470,'Una cucharada',f,'ls','t'); L2=(0.0,80,470+g,'y estás en',f,'ls','t'); L3=(0.0,80,470+2*g,'Tucumán.',f,'ls','t')
fx=lambda l:(-1,)+l[1:]
esc=[(3.4,lambda t:frame(zoom(B21,1.0+0.02*t),[L1,(1.6,)+L2[1:]],t)),
     (2.2,lambda t:frame(zoom(B09,1.0+0.02*t,0.5,0.9),[fx(L1),fx(L2),L3],t)),
     (3.0,lambda t:frame(zoom(B21,1.04),[(0.0,80,470,'Pedí la tuya.',f,'ls','t'),(0.25,82,560,'1 kg a $12.000 y medio kilo a $8.000.',RG(42),'ls','t'),(0.5,80,620,None,None,None,'pills')],t))]
codificar(esc,f'{dR}\\R01 una cucharada.mp4')
frame(B21,[fx(L1),fx(L2),fx(L3)],1).save(f'{dR}\\R01 portada.png')

# ================= R03 · La textura · blanco puro, letra roja =================
dR=f'{C}\\Reels\\R03 La textura\\final'; os.makedirs(dR,exist_ok=True)
def escena_b(n,sc,px,py,ref,seed,sombra='aire'):
    L=LienzoB(W,H,seed=seed); A=colocar(L,n,sc,px,py,ref)
    if sombra=='aire': L.sombra_aire(A,dx=26,dy=34,blur=40,fuerza=0.22)
    elif sombra=='piso': L.sombra_piso(A,py,fuerza=0.30)
    img=L.render(None,None).convert('RGB')
    m=cv2.GaussianBlur(cv2.erode(L.A,np.ones((3,3),np.uint8)),(0,0),1.0)
    return img,m
def zoomm(m,z,cx=0.5,cy=0.5):
    cw,ch=W/z,H/z; x0=(W-cw)*cx; y0=(H-ch)*cy
    return np.asarray(Image.fromarray((m*255).astype(np.uint8)).resize((W,H),Image.BICUBIC,box=(x0,y0,x0+cw,y0+ch))).astype(np.float32)/255
E1=escena_b('10',0.97,540,1920+40,'cb',331,'')
E2=escena_b('22',1.0,540,1560,'cb',332)
E3=escena_b('16',0.90,1080,1640,'rb',333,'piso')
E4=escena_b('11',0.78,540,1920+10,'cb',334,'')
def esc_b(Eb,detras,delante,dur):
    img,m=Eb
    def fn(t):
        z=1.0+0.03*t/dur
        fr=frame(zoom(img,z),detras,t,ROJ,mask=zoomm(m,z))
        return frame(fr,delante,t,ROJ) if delante else fr
    return fn
F1=fit('textura.',950); F2=fit('raspado.',950); F3=fit('fucsia.',950); F4=fit('tucumana.',950)
s1=([(0.15,80,520,'Mirá esta',XB(150),'ls','t'),(0.45,62,830,'textura.',F1,'ls','t')],[])
s2=([(0.15,70,720,'Hielo',fit('Hielo',600),'ls','t')],[(0.45,62,1660,'raspado.',F2,'ls','t')])
s3=([(0.15,80,640,'Color',XB(170),'ls','t'),(0.45,62,960,'fucsia.',F3,'ls','t')],[])
s4=([(0.15,80,640,'Receta',XB(170),'ls','t'),(0.45,62,960,'tucumana.',F4,'ls','t')],[])
blanco=LienzoB(W,H,seed=335).render(None,None).convert('RGB')
def fin03(t): return frame(blanco,[(0.0,540,840,None,560,None,'logo'),(0.3,540,940,'Helado tucumano en Salta.',RG(46),'ms','t'),(0.6,202,1040,None,None,None,'pills')],t,ROJ)
codificar([(2.4,esc_b(E1,*s1,2.4)),(2.4,esc_b(E2,*s2,2.4)),(2.4,esc_b(E3,*s3,2.4)),(2.4,esc_b(E4,*s4,2.4)),(2.6,fin03)],f'{dR}\\R03 la textura.mp4')
esc_b(E1,[(-1,)+i[1:] for i in s1[0]],[],2.4)(0).save(f'{dR}\\R03 portada.png')
print('ok')
