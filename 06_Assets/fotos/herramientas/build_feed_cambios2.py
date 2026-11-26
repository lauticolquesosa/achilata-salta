# Cambios 2 del 26/11/2026 · Lauti no quiso el fondo blanco: P08 y P04 pasan a fondo realista de la propia foto.
# Fotos nuevas de Lauti en 06_Assets/fotos/originales 26-11: 33 Cabildo, 34 cerro, 35 iglesia.
# Uso: python build_feed_cambios2.py [solo_p11]
from feed_comun import *
import subprocess
FPS=30; W,H=S
NUEVAS=RAIZ+r'\06_Assets\fotos\originales 26-11'
def cargar(n):
    fx=os.path.join(RAIZ,'06_Assets','fotos','editadas','fucsia',f'{n}.png')   # versión con el fucsia unificado, si existe
    src=fx if os.path.exists(fx) else glob.glob(NUEVAS+f'/{n} *')[0]
    return np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
def foto(I,Wo,Ho,cx=0.5,cy=0.5,zoom=1.0,seed=7):
    """la foto llena el cuadro sin bandas: se recorta a la proporción, con zoom y centro; una corrección pareja y grano"""
    h,w=I.shape[:2]
    if w/h>Wo/Ho: ch=h/zoom; cw=ch*Wo/Ho
    else: cw=w/zoom; ch=cw*Ho/Wo
    x0=float(np.clip(cx*w-cw/2,0,w-cw)); y0=float(np.clip(cy*h-ch/2,0,h-ch))
    M=np.float32([[Wo/cw,0,-x0*Wo/cw],[0,Ho/ch,-y0*Ho/ch]])
    out=cv2.warpAffine(I,M,(Wo,Ho),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REFLECT)
    out=(out-128)*1.04+128
    g=cv2.GaussianBlur(np.random.default_rng(seed).normal(0,1,(Ho,Wo)).astype(np.float32),(0,0),0.65); g/=g.std()
    return Image.fromarray(np.clip(out+g[...,None]*2.2,0,255).astype(np.uint8))

# ================= P08 · Etiquetá · el pote derritiéndose frente al Cabildo =================
I33=cargar('33')
im=foto(I33,1080,1350,0.5,0.0,1.0,1101).convert('RGBA'); d=ImageDraw.Draw(im)
f=fit('le debés una achilata.',940,mx=120)
T(d,70,150,'Etiquetá a quien',f); T(d,70,150+round(f.size*0.98),'le debés una achilata.',f)
d.text((1010,1300),'y que pague esta vez.',font=INK(50),fill=CREMA,anchor='rs')
d0=f'{C}\\Publicaciones\\P08 Etiquetá a quien le debés\\final'; os.makedirs(d0,exist_ok=True)
im.convert('RGB').save(f'{d0}\\P08 1 etiqueta.png')
if len(sys.argv)>1 and sys.argv[1]=='solo_p11': sys.exit()

# ================= P04 · La textura · el pote en el cerro y frente a la iglesia =================
ease=lambda t:1-(1-min(max(t,0),1))**3
def capa(fr,items,t):
    for t0,x,y,s,f_,an,kind in items:
        if t<t0: continue
        k=ease((t-t0)/0.3); l=Image.new('RGBA',(W,H),(0,0,0,0)); dd=ImageDraw.Draw(l); dy=round(36*(1-k))
        if kind=='pills': numeros(dd,x,y+dy)
        elif kind=='logo':
            lg=logo(f_); l.alpha_composite(lg,(round(x-lg.width/2),round(y-lg.height)+dy))
        elif kind=='ink': dd.text((x,y+dy),s,font=f_,fill=CREMA,anchor=an)
        elif kind=='rg': T(dd,x,y+dy,s,f_,anchor=an,stroke=False)
        else: T(dd,x,y+dy,s,f_,anchor=an)
        if k<1: l.putalpha(l.getchannel('A').point(lambda v:int(v*k)))
        fr.paste(l,(0,0),l)
    return fr
I34=cargar('34'); I35=cargar('35')
# cada toma se renderiza a un poco más de zoom por cuadro: movimiento lento hacia el pote
def toma(I,cx,cy,z0,z1,items,dur):
    return dur,lambda t:capa(foto(I,W,H,cx,cy,z0+(z1-z0)*t/dur,int(t*FPS)+1).convert('RGB'),items,t)
fA=fit('Hay achilata',920,mx=230); fB=fit('raspado.',900,mx=230); fC=fit('fucsia.',900,mx=230); fD=fit('tucumana.',900,mx=230)
fx=lambda l:(-1,)+l[1:]
s1=[(0.15,80,660,'Mirá esta',fA,'ls','t'),(0.45,80,660+round(fA.size*0.9),'textura.',fA,'ls','t')]
s2=[(0.15,80,900,'Hielo',fB,'ls','t'),(0.45,80,900+round(fB.size*0.9),'raspado.',fB,'ls','t')]
s3=[(0.15,80,900,'Color',fC,'ls','t'),(0.45,80,900+round(fC.size*0.9),'fucsia.',fC,'ls','t')]
s4=[(0.15,80,330,'Receta',fD,'ls','t'),(0.45,80,330+round(fD.size*0.9),'tucumana.',fD,'ls','t')]
fin=[(0.0,80,660,'Hay achilata',fA,'ls','t'),(0.25,80,660+round(fA.size*0.9),'en Salta.',fA,'ls','t'),(0.6,80,660+round(fA.size*0.9)+50,None,None,None,'pills')]
esc=[toma(I34,0.5,0.40,1.00,1.05,s1,2.6),
     toma(I34,0.50,0.45,1.8,1.95,s2,2.2),
     toma(I35,0.49,0.36,2.0,2.15,s3,2.2),
     toma(I35,0.49,0.55,1.05,1.10,s4,2.4),
     toma(I34,0.5,0.40,1.05,1.07,fin,3.0)]
dR=f'{C}\\Publicaciones\\P04 La textura\\final'; os.makedirs(dR,exist_ok=True)
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
    '-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',f'{dR}\\P04 la textura.mp4'],stdin=subprocess.PIPE)
for dur,fn in esc:
    for i in range(round(dur*FPS)): p.stdin.write(np.asarray(fn(i/FPS)).tobytes())
p.stdin.close(); p.wait()
capa(foto(I34,W,H,0.5,0.40,1.0,1).convert('RGB'),[fx(l) for l in s1],1).save(f'{dR}\\P04 portada.png')
print('ok')
