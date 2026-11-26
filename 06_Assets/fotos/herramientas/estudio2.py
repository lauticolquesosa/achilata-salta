# Estudio rojo v2: fondo liso con grano, producto recortado y sombras físicas a mano.
# Orden de capas: fondo, texto impreso en el fondo, sombra, producto, texto de adelante.
import os,numpy as np,cv2
from PIL import Image,ImageDraw,ImageFont
FD=r'C:\Users\Lauti\AppData\Local\Microsoft\Windows\Fonts'
XB=lambda s:ImageFont.truetype(FD+r'\BricolageGrotesque-ExtraBold.ttf',s)
RG=lambda s:ImageFont.truetype(FD+r'\BricolageGrotesque-Regular.ttf',s)
INK=lambda s:ImageFont.truetype(r'C:\Windows\Fonts\Inkfree.ttf',s)
CREMA='#FFF3E2'; ROJ='#E7364A'; ROSA='#F3A3B5'
RO=np.array([231,54,74],np.float32)
SOMBRA=np.array([120,14,34],np.float32)   # rojo apagado: lo que el rojo refleja en sombra
LG=r'C:\Users\Lauti\Documents\Proyecto - Achilata\06_Assets\logo'

def logo(w,col='crema'):
    im=Image.open(os.path.join(LG,f'achilata-sin-bajada-{col}.png')).convert('RGBA'); im=im.crop(im.getbbox())
    return im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)

def yfix(im):
    L=cv2.cvtColor(np.clip(im,0,255).astype(np.uint8),cv2.COLOR_RGB2LAB).astype(np.float32)
    yel=np.clip((L[...,2]-140)/12,0,1)*np.clip((142-L[...,1])/8,0,1)
    L[...,1]=L[...,1]+yel*(L[...,2]-128)*0.9; L[...,2]=L[...,2]-yel*(L[...,2]-128)*0.85
    return cv2.cvtColor(np.clip(L,0,255).astype(np.uint8),cv2.COLOR_LAB2RGB).astype(np.float32)

def cut(V,n,flip=False):
    a=np.load(f'{V}/a{n}.npy').astype(np.float32); F=np.load(f'{V}/f{n}.npy').astype(np.float32)
    if n in ('02','13'): F=yfix(F)
    if flip: a=a[:,::-1].copy(); F=F[:,::-1].copy()
    return F,a

class Lienzo:
    def __init__(s,W,H,seed=3):
        s.W,s.H=W,H
        g=cv2.GaussianBlur(np.random.default_rng(seed).normal(0,1,(H,W)).astype(np.float32),(0,0),0.7); g/=g.std()
        s.bg=np.zeros((H,W,3),np.float32)+RO+g[...,None]*1.5
        s.sh=np.zeros((H,W),np.float32)
        s.F=np.zeros((H,W,3),np.float32); s.A=np.zeros((H,W),np.float32)
        s.front=[]; s.back=[]
        s.suave=1.0   # bordes del recorte: 1 es el método de H05; 1.8 o más los difumina para que no se vea mal cortado
    def poner(s,F,a,scale,x,y):
        """pega el recorte escalado con su esquina arriba izquierda en x,y; devuelve la máscara en el lienzo"""
        h,w=a.shape; nw,nh=round(w*scale),round(h*scale)
        it=cv2.INTER_AREA if scale<1 else cv2.INTER_LANCZOS4
        Fs=cv2.resize(F,(nw,nh),interpolation=it); As=np.clip(cv2.resize(a,(nw,nh),interpolation=it),0,1)
        X0,Y0=max(0,x),max(0,y); X1,Y1=min(s.W,x+nw),min(s.H,y+nh)
        sx,sy=X0-x,Y0-y
        As_=As[sy:sy+Y1-Y0,sx:sx+X1-X0]; Fs_=Fs[sy:sy+Y1-Y0,sx:sx+X1-X0]
        A=np.zeros((s.H,s.W),np.float32); A[Y0:Y1,X0:X1]=As_
        s.F[Y0:Y1,X0:X1]=Fs_*As_[...,None]+s.F[Y0:Y1,X0:X1]*(1-As_[...,None])
        s.A=np.maximum(s.A,A)
        return A
    def sombra_piso(s,A,base_y,largo=0.42,inclina=0.75,fuerza=0.42):
        """objeto apoyado: sombra proyectada hacia la derecha y atrás, contacto oscuro y oclusión"""
        ys,xs=np.where(A>0.5); x0,x1=xs.min(),xs.max(); top=ys.min(); hgt=base_y-top
        sil=(A>0.5).astype(np.float32)
        src=np.float32([[x0,base_y],[x1,base_y],[x0,top]])
        dst=np.float32([[x0,base_y],[x1,base_y],[x0+hgt*inclina,base_y-hgt*largo]])
        M=cv2.getAffineTransform(src,dst)
        p=cv2.warpAffine(sil,M,(s.W,s.H)); p[base_y+2:]=0
        # penumbra que se abre con la distancia a la base
        d=np.clip((base_y-np.arange(s.H)[:,None])/max(1,hgt*largo),0,1)
        b1=cv2.GaussianBlur(p,(0,0),3); b2=cv2.GaussianBlur(p,(0,0),16); b3=cv2.GaussianBlur(p,(0,0),34)
        cast=b1*(1-d)**2+b2*2*d*(1-d)+b3*d**2
        cast=cast*(1-0.55*d)
        # sombra de contacto: delgada y oscura justo debajo del borde
        w=(x1-x0)
        con=np.zeros((s.H,s.W),np.float32)
        cv2.ellipse(con,((x0+x1)//2,base_y-3),(int(w*0.47),max(6,int(w*0.022))),0,0,360,1,-1)
        con=cv2.GaussianBlur(con,(0,0),max(3,w*0.012))
        ao=np.zeros((s.H,s.W),np.float32)
        cv2.ellipse(ao,((x0+x1)//2+int(w*0.06),base_y),(int(w*0.62),int(w*0.07)),0,0,360,1,-1)
        ao=cv2.GaussianBlur(ao,(0,0),w*0.05)
        s.sh=np.maximum(s.sh,np.clip(cast*fuerza+con*0.62+ao*0.22,0,0.85))
    def sombra_aire(s,A,dx=34,dy=44,blur=30,fuerza=0.28):
        """objeto en la mano, cerca del fondo: sombra suave corrida hacia abajo a la derecha"""
        M=np.float32([[1,0,dx],[0,1,dy]])
        p=cv2.warpAffine((A>0.5).astype(np.float32),M,(s.W,s.H))
        p=cv2.GaussianBlur(p,(0,0),blur)*0.75+cv2.GaussianBlur(p,(0,0),blur*0.35)*0.25
        s.sh=np.maximum(s.sh,p*fuerza)
    def integrar(s,b):
        """Que el recorte no parezca pegado: saca el halo, cierra la máscara, envuelve el borde con la luz
        del fondo, suma rebote rojo y unifica el grano. b es el fondo ya con texto y sombra."""
        A=s.A.copy(); F=s.F.copy()
        # 1 · defringe: el borde toma el color de adentro del objeto, no el del fondo original
        core=cv2.erode((A>0.97).astype(np.uint8),np.ones((5,5),np.uint8)).astype(np.float32)
        num=cv2.GaussianBlur(F*core[...,None],(0,0),3); den=cv2.GaussianBlur(core,(0,0),3)[...,None]
        inner=num/np.maximum(den,1e-4)
        band=np.clip((0.985-A)/0.4,0,1)*(A>0.01)*(den[...,0]>0.02)
        band=cv2.GaussianBlur(band,(0,0),1.2)[...,None]
        F=F*(1-band)+inner*band
        # 2 · máscara: se cierra un pixel y se suaviza apenas, como un borde óptico
        A=cv2.erode(A,np.ones((3,3),np.uint8)); A=cv2.GaussianBlur(A,(0,0),0.9*s.suave)
        # 3 · light wrap: la luz roja del fondo se mete en el borde del objeto
        bgb=cv2.GaussianBlur(b,(0,0),14)
        wrap=cv2.GaussianBlur(1-A,(0,0),7*s.suave)*A
        lw=min(0.7,0.55*s.suave**0.4)
        F=F*(1-wrap[...,None]*lw)+bgb*wrap[...,None]*lw
        # 4 · rebote: el rojo del estudio tiñe un poco las zonas en sombra del objeto
        lum=F.mean(-1,keepdims=True)/255
        k=0.10*np.clip(1-lum,0,1)**1.2
        F=F*(1-k)+(F*RO/RO.max())*k
        out=F*A[...,None]+b*(1-A[...,None])
        # 5 · un solo grano para todo, como si fuera una sola foto
        g=cv2.GaussianBlur(np.random.default_rng(99).normal(0,1,out.shape[:2]).astype(np.float32),(0,0),0.6); g/=g.std()
        return out+g[...,None]*2.2
    def render(s,atras=None,adelante=None,natural=True):
        base=Image.fromarray(np.clip(s.bg,0,255).astype(np.uint8)).convert('RGBA')
        if atras: atras(ImageDraw.Draw(base),base)
        b=np.asarray(base.convert('RGB')).astype(np.float32)
        k=s.sh[...,None]
        # multiplicar hacia el rojo profundo, no hacia el negro: la sombra conserva color
        tint=SOMBRA/255.0
        b=b*(1-k)+b*tint*1.9*k
        out=s.integrar(b) if natural else s.F*s.A[...,None]+b*(1-s.A[...,None])
        img=Image.fromarray(np.clip(out,0,255).astype(np.uint8)).convert('RGBA')
        if adelante: adelante(ImageDraw.Draw(img),img)
        return img.convert('RGB')

def T(d,x,y,t,f,anchor='ls',stroke=True,fill=CREMA,track=0):
    sw=max(1,round(f.size*0.022)) if stroke else 0
    if not track:
        d.text((x,y),t,font=f,fill=fill,anchor=anchor,stroke_width=sw,stroke_fill=fill); return
    for ch in t:
        d.text((x,y),ch,font=f,fill=fill,anchor=anchor,stroke_width=sw,stroke_fill=fill)
        x+=d.textlength(ch,font=f)+track
def ancho(t,f,track=0):
    d=ImageDraw.Draw(Image.new('L',(1,1)))
    return d.textlength(t,font=f)+track*(len(t)-1)
def bbox(A):
    ys,xs=np.where(A>0.5); return xs.min(),ys.min(),xs.max(),ys.max()
