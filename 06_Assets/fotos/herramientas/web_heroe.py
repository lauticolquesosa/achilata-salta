# Fotos del héroe de la web: el pote recortado con el método integrado del estudio rojo, en PNG con transparencia,
# para que se funda con el rojo liso del héroe. Uso: python web_heroe.py carpeta_de_recortes carpeta_salida
import sys,os,numpy as np,cv2
from PIL import Image
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from estudio2 import Lienzo,cut,RO,SOMBRA
V,O=sys.argv[1],sys.argv[2]; os.makedirs(O,exist_ok=True)

def capas(L):
    """lo mismo que integrar(), pero devuelve el objeto y la sombra por separado sobre un rojo liso"""
    k=L.sh; b=np.zeros_like(L.bg)+RO; b=b*(1-k[...,None])+b*(SOMBRA/255*1.9)*k[...,None]
    A=L.A.copy(); F=L.F.copy()
    core=cv2.erode((A>0.97).astype(np.uint8),np.ones((5,5),np.uint8)).astype(np.float32)
    num=cv2.GaussianBlur(F*core[...,None],(0,0),3); den=cv2.GaussianBlur(core,(0,0),3)[...,None]
    inner=num/np.maximum(den,1e-4)
    band=np.clip((0.985-A)/0.4,0,1)*(A>0.01)*(den[...,0]>0.02)
    band=cv2.GaussianBlur(band,(0,0),1.2)[...,None]
    F=F*(1-band)+inner*band
    A=cv2.erode(A,np.ones((3,3),np.uint8)); A=cv2.GaussianBlur(A,(0,0),0.9)
    wrap=cv2.GaussianBlur(1-A,(0,0),7)*A
    F=F*(1-wrap[...,None]*0.55)+cv2.GaussianBlur(b,(0,0),14)*wrap[...,None]*0.55
    lum=F.mean(-1,keepdims=True)/255; kk=0.10*np.clip(1-lum,0,1)**1.2
    F=F*(1-kk)+(F*RO/RO.max())*kk
    g=cv2.GaussianBlur(np.random.default_rng(99).normal(0,1,F.shape[:2]).astype(np.float32),(0,0),0.6); g/=g.std()
    F=F+g[...,None]*2.2
    S=RO*SOMBRA/255*1.9
    a=A+k*(1-A)
    rgb=(F*A[...,None]+S*(k*(1-A))[...,None])/np.maximum(a[...,None],1e-4)
    im=np.dstack([np.clip(rgb,0,255),np.clip(a*255,0,255)]).astype(np.uint8)
    return Image.fromarray(im,'RGBA')

def guardar(im,nombre):
    im=im.crop(im.getchannel('A').point(lambda v:255 if v>2 else 0).getbbox())
    im.save(f'{O}/{nombre}.png'); print(nombre,im.size)

# escritorio: el pote de tres bochas sube desde el borde de abajo
F,a=cut(V,'11'); h,w=a.shape
L=Lienzo(w+400,h+200,seed=5); A=L.poner(F,a,1,200,200)
L.sombra_aire(A,dx=40,dy=0,blur=46,fuerza=0.30)
guardar(capas(L),'heroe-pote')

# celular: el pote entero con la cuchara, apoyado, con su sombra de piso
F,a=cut(V,'16'); ys,xs=np.where(a>0.5); base=ys.max()
L=Lienzo(a.shape[1]+900,a.shape[0]+400,seed=6); A=L.poner(F,a,1,200,300)
L.sombra_piso(A,base+300)
guardar(capas(L),'heroe-pote-movil')

# el del celular se centra en el pote, así la sombra larga hacia la derecha no lo corre del medio
im=Image.open(f'{O}/heroe-pote-movil.png'); al=np.array(im.getchannel('A'))
xs=np.where(al.max(0)>200)[0]; c=(xs.min()+xs.max())/2; half=int(max(c,im.width-c))
n=Image.new('RGBA',(2*half,im.height),(0,0,0,0)); n.paste(im,(int(half-c),0)); n.save(f'{O}/heroe-pote-movil.png'); print('centrado',n.size)
