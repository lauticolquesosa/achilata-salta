import sys,os,glob,numpy as np,cv2
sys.path.insert(0,r'C:\Users\Lauti\Documents\Proyecto - Achilata\06_Assets\fotos\herramientas')
from studio import *
from PIL import Image,ImageDraw,ImageFont
V=sys.argv[1]; O=sys.argv[2]; os.makedirs(O,exist_ok=True)
FD=r'C:\Users\Lauti\AppData\Local\Microsoft\Windows\Fonts'
XB=lambda s:ImageFont.truetype(FD+r'\BricolageGrotesque-ExtraBold.ttf',s)
RG=lambda s:ImageFont.truetype(FD+r'\BricolageGrotesque-Regular.ttf',s)
INK=lambda s:ImageFont.truetype(r'C:\Windows\Fonts\Inkfree.ttf',s)
W_='#FFFFFF'; ROJ='#E7364A'
LG=r'C:\Users\Lauti\Documents\Proyecto - Achilata\06_Assets\logo'
def logo(w):
    im=Image.open(os.path.join(LG,'achilata-sin-bajada-blanco.png')).convert('RGBA'); im=im.crop(im.getbbox())
    return im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
def yfix(im):
    L=cv2.cvtColor(np.clip(im,0,255).astype(np.uint8),cv2.COLOR_RGB2LAB).astype(np.float32)
    yel=np.clip((L[...,2]-140)/12,0,1)*np.clip((142-L[...,1])/8,0,1)
    L[...,1]=L[...,1]+yel*(L[...,2]-128)*0.9; L[...,2]=L[...,2]-yel*(L[...,2]-128)*0.85
    return cv2.cvtColor(np.clip(L,0,255).astype(np.uint8),cv2.COLOR_LAB2RGB).astype(np.float32)
def src(n,flip=False):
    im=np.asarray(Image.open(f'{V}/src{n}.png').convert('RGB')).astype(np.float32); a=np.load(f'{V}/a{n}.npy'); Fo=np.load(f'{V}/f{n}.npy')
    if n in ('02','13'): im=yfix(im); Fo=yfix(Fo)
    if flip: im=im[:,::-1].copy(); a=a[:,::-1].copy(); Fo=Fo[:,::-1].copy()
    return im,a,Fo
def frame(n,box,size,flip=False,gamma=1.0):
    im,a,Fo=src(n,flip); H,W=a.shape; x0,y0,x1,y1=box
    T,B,L,R=max(0,-y0),max(0,y1-H),max(0,-x0),max(0,x1-W)
    bg,F,A=studio(im,a,T,B,L,R,gamma=gamma,Fo=Fo)
    cx0,cy0=x0+L,y0+T; sl=(slice(cy0,cy0+(y1-y0)),slice(cx0,cx0+(x1-x0)))
    rs=lambda z:cv2.resize(z[sl],size,interpolation=cv2.INTER_AREA if (x1-x0)>size[0] else cv2.INTER_LANCZOS4)
    return rs(bg),rs(F),np.clip(rs(A),0,1)
def T(d,x,y,t,f,anchor='ls',stroke=True,fill=W_):
    sw=max(1,round(f.size*0.015)) if stroke else 0
    d.text((x,y),t,font=f,fill=fill,anchor=anchor,stroke_width=sw,stroke_fill=fill)
def compose(bg,F,A,text_fn=None,front_fn=None):
    base=Image.fromarray(np.clip(bg,0,255).astype(np.uint8)).convert('RGBA')
    if text_fn: text_fn(ImageDraw.Draw(base),base)
    b=np.asarray(base.convert('RGB')).astype(np.float32)
    out=F*A[...,None]+b*(1-A[...,None])
    img=Image.fromarray(np.clip(out,0,255).astype(np.uint8)).convert('RGBA')
    if front_fn: front_fn(ImageDraw.Draw(img),img)
    return img.convert('RGB')
def grain(H,W,seed=5):
    g=cv2.GaussianBlur(np.random.default_rng(seed).normal(0,1,(H,W)).astype(np.float32),(0,0),0.7); return g/g.std()
RO=np.array([231,54,74],np.float32)
P=(1080,1350); S=(1080,1920)

# ================= H02 1 · envíos · foto 14 =================
im,a,Fo=src('14'); H,W=a.shape
yy,xx=np.mgrid[0:H,0:W]
# sacar el saco: zona oscura a la izquierda, debajo de la mano de la cuchara
L=lab(im)[...,0]
jacket=((xx<312)&(yy>640)) | ((xx<355)&(yy>975)) | ((yy>1180)&(xx<370))
jacket |= (yy>1250)&(xx>540)
a2=a.copy(); a2[jacket]=0
Y1=1170  # corte abajo: la muñeca sale del cuadro
a2=a2[:Y1]; F2=Fo[:Y1]
sc=1080/W; h=round(Y1*sc)
aa=cv2.resize(a2,(1080,h),interpolation=cv2.INTER_AREA); ff=cv2.resize(F2,(1080,h),interpolation=cv2.INTER_AREA)
# limpiar restos sueltos del saco
hard=(aa>0.5).astype(np.uint8); n,lb,st,_=cv2.connectedComponentsWithStats(hard)
keep=np.zeros_like(hard)
for i in range(1,n):
    if st[i,4]>20000: keep[lb==i]=1
aa=aa*cv2.dilate(keep,np.ones((7,7),np.uint8))
oy=1920-h
sky=(ff[...,2]>ff[...,0]+25)&(ff[...,2]>ff[...,1]+5)
sky=cv2.GaussianBlur(cv2.dilate(sky.astype(np.uint8),np.ones((3,3),np.uint8)).astype(np.float32),(0,0),1.0)
sky[:1660-oy]=0
aa=aa*(1-sky)
A=np.zeros((1920,1080),np.float32); A[oy:]=aa
Lb=cv2.cvtColor(np.clip(ff,0,255).astype(np.uint8),cv2.COLOR_RGB2LAB).astype(np.float32)
blue=np.clip((124-Lb[...,2])/10,0,1)*(aa<0.995)
Lb[...,2]=Lb[...,2]+blue*(140-Lb[...,2]); Lb[...,1]=Lb[...,1]+blue*(142-Lb[...,1])*0.5
ff=cv2.cvtColor(Lb.astype(np.uint8),cv2.COLOR_LAB2RGB).astype(np.float32)
Fc=np.zeros((1920,1080,3),np.float32); Fc[oy:]=ff
bg=np.zeros((1920,1080,3),np.float32)+RO+grain(1920,1080)[...,None]*1.4
def t(d,im_):
    lg=logo(170); im_.alpha_composite(lg,(80,250))
    f=XB(138); T(d,80,560,'Hoy hacemos',f); T(d,80,692,'envíos.',f)
def fr(d,im_):
    T(d,82,790,'Consultanos por tu zona.',RG(44),stroke=False)
compose(bg,Fc,A,t,fr).save(f'{O}/H02 1 envios.png')
np.save(f'{V}/A14_story.npy',A)

# ================= H02 2 · calor · foto 08 con sol duro =================
im,a,Fo=src('08'); H,W=a.shape
ys,xs=np.where(a>0.05); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
a8=a[y0:y1,x0:x1]; F8=Fo[y0:y1,x0:x1]
cw=620; ch=round(a8.shape[0]*cw/a8.shape[1])
aa=cv2.resize(a8,(cw,ch),interpolation=cv2.INTER_AREA); ff=cv2.resize(F8,(cw,ch),interpolation=cv2.INTER_AREA)
rows=(aa_tmp:=cv2.resize(a8,(cw,ch),interpolation=cv2.INTER_AREA)>0.5).sum(1); bot=int(np.where(rows>0.3*cw)[0].max())
cx=420; base_y=1520; X=cx-cw//2; Y=base_y-bot
A=np.zeros((1920,1080),np.float32); A[Y:Y+ch,X:X+cw]=aa
Fc=np.zeros((1920,1080,3),np.float32); Fc[Y:Y+ch,X:X+cw]=ff
# sombra de sol de siesta: proyectada hacia la derecha y abajo, larga y dura
sil=(A>0.5).astype(np.float32)
src_pts=np.float32([[X,base_y],[X+cw,base_y],[X,Y]])
dst_pts=np.float32([[X,base_y],[X+cw,base_y],[X+cw*0.62,base_y-bot*0.42]])
M=cv2.getAffineTransform(src_pts,dst_pts)
sh=cv2.warpAffine(sil,M,(1080,1920))
sh=np.maximum(sh,0); sh=cv2.GaussianBlur(sh,(0,0),3.0)
# leve ablandamiento lejos de la base, como sol real
dist=np.clip((base_y-np.arange(1920)[:,None])/(bot*0.42),0,1)
sh=sh*(1-0.25*dist)
contact=np.zeros((1920,1080),np.float32)
cv2.ellipse(contact,(cx,base_y-4),(int(cw*0.40),16),0,0,360,1,-1)
contact=cv2.GaussianBlur(contact,(0,0),8)
shade=1-np.clip(sh*0.26+contact*0.45,0,0.6)
bg=RO[None,None,:]*shade[...,None]+grain(1920,1080,9)[...,None]*1.4
def t(d,im_):
    f=XB(170); T(d,80,420,'Achilata',f); T(d,80,575,'hoy.',f)
def fr(d,im_):
    T(d,82,680,'Para la siesta, para el calor,',RG(42),stroke=False)
    T(d,82,736,'para Salta en noviembre.',RG(42),stroke=False)
    d.text((80,1640),'la ciudad se derrite, vos no.',font=INK(52),fill=W_)
    lg=logo(170); im_.alpha_composite(lg,(1000-170,1672-lg.height))
compose(bg,Fc,A,t,fr).save(f'{O}/H02 2 achilata hoy.png')

# ================= P02 El menú =================
bg,F,A=frame('28',(-330,-330,1354,1775),P,gamma=0.35)
def t(d,im_): T(d,80,330,'El menú.',XB(220))
def fr(d,im_):
    d.text((84,392),'corto, como tiene que ser.',font=INK(50),fill=W_)
    lg=logo(190); im_.alpha_composite(lg,(80,1350-80-lg.height))
compose(bg,F,A,t,fr).save(f'{O}/P02 1 el menu.png')

bg,F,A=frame('11',(-330,-600,1441,1614),P)
def fr(d,im_):
    T(d,80,250,'1 kg.',XB(200))
    T(d,82,370,'$12.000',XB(96))
    T(d,82,440,'Para la mesa entera.',RG(40),stroke=False)
compose(bg,F,A,None,fr).save(f'{O}/P02 2 un kilo.png')

bg,F,A=frame('02',(-128,-430,1152,1170),P)
def fr(d,im_):
    T(d,80,230,'Medio kilo.',XB(150))
    T(d,82,345,'$8.000',XB(96))
    T(d,82,415,'Para vos y alguien más.',RG(40),stroke=False)
compose(bg,F,A,None,fr).save(f'{O}/P02 3 medio kilo.png')

bg,F,A=frame('16',(-330,-1000,1424,1193),P,gamma=0.55)
def pill(d,x,y,w,h,text,font):
    d.rounded_rectangle((x,y,x+w,y+h),radius=h//2,fill=W_)
    d.text((x+w/2,y+h/2),text,font=font,fill=ROJ,anchor='mm')
def fr(d,im_):
    T(d,80,200,'Cómo pedir.',XB(130))
    f=RG(40)
    for i,s in enumerate(['Escribinos por WhatsApp.','Elegí tu pote.','Te la llevamos a casa.']):
        T(d,82,290+i*56,s,f,stroke=False)
    pill(d,80,480,450,88,'387 483 4041',XB(44)); pill(d,550,480,450,88,'387 468 4498',XB(44))
    for i,s in enumerate(['Delivery en Grand Bourg, San Lorenzo Chico,','San Lorenzo, El Tipal y La Almudena.','Transferencia o efectivo.']):
        T(d,82,650+i*46,s,RG(32),stroke=False)
    lg=logo(170); im_.alpha_composite(lg,(80,1350-80-lg.height))
compose(bg,F,A,None,fr).save(f'{O}/P02 4 como pedir.png')

# hojas de control
fs=sorted(glob.glob(f'{O}/H02 *.png')); s=Image.new('RGB',(2*540+30,970),'#777')
for i,p in enumerate(fs): s.paste(Image.open(p).resize((540,960)),(10+i*550,5))
s.save(f'{V}/../sheetH02.jpg',quality=88)
fs=sorted(glob.glob(f'{O}/P02 *.png')); s=Image.new('RGB',(4*432+50,560),'#777')
for i,p in enumerate(fs): s.paste(Image.open(p).resize((432,540)),(10+i*442,10))
s.save(f'{V}/../sheetP02.jpg',quality=88)
