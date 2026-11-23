import sys,os,glob,numpy as np,cv2
sys.path.insert(0,r'C:\Users\Lauti\Documents\Proyecto - Achilata\06_Assets\fotos\herramientas')
from studio import *
from extend import extend
from PIL import Image,ImageDraw,ImageFont,ImageFilter
V=sys.argv[1]; O=sys.argv[2]; os.makedirs(O,exist_ok=True)
ORIG=r'C:\Users\Lauti\Documents\Proyecto - Achilata\06_Assets\fotos\originales 19-11'
FD=r'C:\Users\Lauti\AppData\Local\Microsoft\Windows\Fonts'
XB=lambda s:ImageFont.truetype(FD+r'\BricolageGrotesque-ExtraBold.ttf',s)
RG=lambda s:ImageFont.truetype(FD+r'\BricolageGrotesque-Regular.ttf',s)
INK=lambda s:ImageFont.truetype(r'C:\Windows\Fonts\Inkfree.ttf',s)
BL='#FFFFFF'; ROJ='#E7364A'; BOR='#3A1320'
CREMA=np.array([0xFF,0xF3,0xE2],np.float32); RO=np.array([231,54,74],np.float32)
LG=r'C:\Users\Lauti\Documents\Proyecto - Achilata\06_Assets\logo'
def logo(w,col='blanco'):
    im=Image.open(os.path.join(LG,f'achilata-sin-bajada-{col}.png')).convert('RGBA'); im=im.crop(im.getbbox())
    return im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
def T(d,x,y,t,f,anchor='ls',stroke=True,fill=BL):
    sw=max(1,round(f.size*0.015)) if stroke else 0
    d.text((x,y),t,font=f,fill=fill,anchor=anchor,stroke_width=sw,stroke_fill=fill)
def grain(H,W,seed=5):
    g=cv2.GaussianBlur(np.random.default_rng(seed).normal(0,1,(H,W)).astype(np.float32),(0,0),0.7); return g/g.std()
def pill(d,x,y,w,h,text,font,bg,fg):
    d.rounded_rectangle((x,y,x+w,y+h),radius=h//2,fill=bg)
    d.text((x+w/2,y+h/2+2),text,font=font,fill=fg,anchor='mm')

# ================= H05 1 · salimos a repartir · foto 15 =================
im=Image.open(os.path.join(ORIG,'15 Pila de helados Achilata.png')).convert('RGB')
w15=1080; h15=round(im.height*w15/im.width)          # 1314, apenas reducida
ph=im.resize((w15,h15),Image.LANCZOS)
ph=ph.filter(ImageFilter.UnsharpMask(radius=1.2,percent=40,threshold=2))
# grade suave: un poco más de calidez y contraste, el rojo del delantal hacia el rojo achilata
a=np.asarray(ph).astype(np.float32)
a=np.clip((a-128)*1.04+128+np.array([3,0,-3]),0,255)
ph=Image.fromarray(a.astype(np.uint8))
PY=700
canvas=Image.fromarray(np.clip(RO+grain(1920,1080)[...,None]*1.4,0,255).astype(np.uint8))
canvas.paste(ph.crop((0,0,1080,1920-PY)),(0,PY))
d=ImageDraw.Draw(canvas)
f=XB(150); T(d,80,400,'Hoy salimos',f); T(d,80,540,'a repartir.',f)
for i,s in enumerate(['Envíos a Grand Bourg, San Lorenzo Chico,','San Lorenzo, El Tipal y La Almudena.']):
    T(d,82,612+i*46,s,RG(36),stroke=False)
canvas.save(f'{O}/H05 1 salimos a repartir.png')

# ================= H05 2 · pedidos al · foto 01 con su fondo, banda crema arriba =================
im=Image.open(os.path.join(ORIG,'01 Copa de sorbete fucsia Achilata (1).png')).convert('RGB')
ph=im.resize((1080,round(im.height*1080/im.width)),Image.LANCZOS)
ph=ph.filter(ImageFilter.UnsharpMask(radius=1.2,percent=35,threshold=2))
PY=720; CT=230
st=Image.fromarray(np.clip(CREMA+grain(1920,1080,11)[...,None]*1.2,0,255).astype(np.uint8))
st.paste(ph.crop((0,CT,1080,CT+1920-PY)),(0,PY))
d=ImageDraw.Draw(st)
T(d,80,420,'Pedidos al',XB(160),fill=ROJ)
pill(d,80,470,450,96,'387 483 4041',XB(48),ROJ,BL)
pill(d,550,470,450,96,'387 468 4498',XB(48),ROJ,BL)
T(d,82,628,'Escribinos y te la llevamos a casa.',RG(40),stroke=False,fill=BOR)
st.save(f'{O}/H05 2 pedidos al.png')

# ================= P08 · Achilata, sustantivo · foto 10 sobre crema =================
im=np.asarray(Image.open(f'{V}/src10.png').convert('RGB')).astype(np.float32)
a=np.load(f'{V}/a10.npy'); Fo=np.load(f'{V}/f10.npy')
Lp,Tp=606,509
bg,F,A=studio(im,a,Tp,0,Lp,0,gamma=0.8,color=CREMA,grain=1.4,Fo=Fo)
H,W=A.shape; sc=1080/W; h=round(H*sc)
rs=lambda z:cv2.resize(z,(1080,h),interpolation=cv2.INTER_AREA)
bg,F,A=rs(bg)[h-1350:],rs(F)[h-1350:],np.clip(rs(A),0,1)[h-1350:]
base=Image.fromarray(np.clip(bg,0,255).astype(np.uint8)).convert('RGBA')
out=F*A[...,None]+np.asarray(base.convert('RGB')).astype(np.float32)*(1-A[...,None])
img=Image.fromarray(np.clip(out,0,255).astype(np.uint8)).convert('RGBA')
d=ImageDraw.Draw(img)
T(d,76,250,'achilata',XB(200),fill=ROJ)
T(d,82,320,'a·chi·la·ta · sustantivo femenino.',RG(38),stroke=False,fill=BOR)
for i,s in enumerate(['Helado de agua tucumano, color fucsia.','Se come con calor y en buena compañía.']):
    T(d,82,396+i*50,s,RG(38),stroke=False,fill=BOR)
d.text((80,1080),'dicen que viene de',font=INK(46),fill=ROJ)
d.text((80,1136),'hay gelata.',font=INK(46),fill=ROJ)
lg=logo(170,'rojo'); img.alpha_composite(lg,(80,1270-lg.height+0))
img.convert('RGB').save(f'{O}/P08 achilata sustantivo.png')
