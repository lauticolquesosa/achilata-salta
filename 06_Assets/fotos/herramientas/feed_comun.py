# Piezas comunes del feed completo del 26/11/2026, modelo Rocambolesc:
# fondo rojo achilata liso, letra crema, palabra gigante pisada por el producto y macros a sangre.
import sys,os,glob
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from estudio2 import *

RAIZ=r'C:\Users\Lauti\Documents\Proyecto - Achilata'
ORIG=RAIZ+r'\06_Assets\fotos\originales 19-11'
C=RAIZ+r'\04_Contenido'
P=(1080,1350); S=(1080,1920)

def fit(t,w,fn=XB,mx=700):
    s=mx
    while ancho(t,fn(s))>w: s-=2
    return fn(s)

def pill(d,x,y,w,h,text,font,fill=CREMA,col=ROJ):
    d.rounded_rectangle((x,y,x+w,y+h),radius=h//2,fill=fill)
    d.text((x+w/2,y+h/2+2),text,font=font,fill=col,anchor='mm')

def numeros(d,x,y,h=66,w=330,gap=16):
    pill(d,x,y,w,h,'387 483 4041',XB(round(h*0.48)))
    pill(d,x+w+gap,y,w,h,'387 468 4498',XB(round(h*0.48)))

def poner_logo(im,x,y_base,w=160,col='crema'):
    lg=logo(w,col); im.alpha_composite(lg,(x,y_base-lg.height))

def orig(n):
    f=glob.glob(ORIG+f'/{n} *.png')[0]
    return np.asarray(Image.open(f).convert('RGB')).astype(np.float32)

def macro(n,W,H,cx,cy,zoom,oscurecer=0.0,seed=5):
    """foto original a sangre: recorte centrado en cx,cy (0 a 1) con zoom, una sola corrección pareja y grano.
    Sin degradé: el oscurecido es uniforme en toda la foto."""
    I=orig(n); h,w=I.shape[:2]
    cw=w/zoom; ch=cw*H/W
    if ch>h: ch=h/zoom; cw=ch*W/H
    x0=int(np.clip(cx*w-cw/2,0,w-cw)); y0=int(np.clip(cy*h-ch/2,0,h-ch))
    crop=I[y0:int(y0+ch),x0:int(x0+cw)]
    out=cv2.resize(crop,(W,H),interpolation=cv2.INTER_LANCZOS4)
    # contraste suave y un poco más cálido, para que el fucsia hable con el rojo de la marca
    out=(out-128)*1.06+128; out[...,0]*=1.02; out[...,2]*=0.98
    out=out*(1-oscurecer)
    out=cv2.detailEnhance(np.clip(out,0,255).astype(np.uint8),sigma_s=6,sigma_r=0.12).astype(np.float32)*0.35+out*0.65
    g=cv2.GaussianBlur(np.random.default_rng(seed).normal(0,1,(H,W)).astype(np.float32),(0,0),0.65); g/=g.std()
    out=out+g[...,None]*3.0
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8)).convert('RGBA')

def hoja(paths,out,w=432,h=540,cols=None):
    cols=cols or len(paths); rows=(len(paths)+cols-1)//cols
    s=Image.new('RGB',(cols*(w+10)+10,rows*(h+10)+10),'#777')
    for i,p in enumerate(paths):
        s.paste(Image.open(p).convert('RGB').resize((w,h),Image.LANCZOS),(10+(i%cols)*(w+10),10+(i//cols)*(h+10)))
    s.save(out,quality=88)
