import sys,os,numpy as np,cv2
from PIL import Image,ImageDraw,ImageFont
V=sys.argv[1]; OUT=sys.argv[2]
FD=r'C:\Users\Lauti\AppData\Local\Microsoft\Windows\Fonts'
XB=lambda s:ImageFont.truetype(FD+r'\BricolageGrotesque-ExtraBold.ttf',s)
RG=lambda s:ImageFont.truetype(FD+r'\BricolageGrotesque-Regular.ttf',s)
INK=lambda s:ImageFont.truetype(r'C:\Windows\Fonts\Inkfree.ttf',s)
ROJ=np.array([231,54,74],np.float32); W,H=1080,1920
a=np.load(f'{V}/a28.npy'); F=np.load(f'{V}/f28.npy')
ys,xs=np.where(a>0.02); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
a=a[y0:y1,x0:x1]; F=F[y0:y1,x0:x1]
rng=np.random.default_rng(3)
bg=np.zeros((H,W,3),np.float32)+ROJ
shade=np.ones((H,W),np.float32)
cups=[]
def cup(w,cx,bottom):
    h=round(a.shape[0]*w/a.shape[1])
    aa=cv2.resize(a,(w,h),interpolation=cv2.INTER_AREA); ff=cv2.resize(F,(w,h),interpolation=cv2.INTER_AREA)
    x=cx-w//2; y=bottom-h
    # contact + soft cast shadow
    sh=np.zeros((H,W),np.float32)
    cv2.ellipse(sh,(cx,bottom-int(w*0.035)),(int(w*0.37),int(w*0.05)),0,0,360,1,-1)
    soft=np.zeros((H,W),np.float32)
    cv2.ellipse(soft,(cx+int(w*0.08),bottom-int(w*0.02)),(int(w*0.55),int(w*0.08)),0,0,360,1,-1)
    m=cv2.GaussianBlur(sh,(0,0),w*0.02)*0.55+cv2.GaussianBlur(soft,(0,0),w*0.07)*0.35
    global shade; shade=shade*(1-m)
    cups.append((ff,aa,x,y))
cup(545,345,1290)
cup(365,825,1290)
g=cv2.GaussianBlur(rng.normal(0,1,(H,W)).astype(np.float32),(0,0),0.7); g/=g.std()
img=bg*shade[...,None]+g[...,None]*1.4
base=Image.fromarray(np.clip(img,0,255).astype(np.uint8)).convert('RGBA')
d=ImageDraw.Draw(base)
def T(x,y,t,f,anchor='ls',stroke=True,fill='#FFFFFF'):
    sw=max(1,round(f.size*0.015)) if stroke else 0
    d.text((x,y),t,font=f,fill=fill,anchor=anchor,stroke_width=sw,stroke_fill=fill)
# behind-the-cup typography
T(80,400,'Elegí tu pote.',XB(132)); T(82,478,'Sabor clásico, el de siempre.',RG(40),stroke=False)
out=np.asarray(base.convert('RGB')).astype(np.float32)
for ff,aa,x,y in cups:
    h,w=aa.shape; reg=out[y:y+h,x:x+w]
    out[y:y+h,x:x+w]=ff*aa[...,None]+reg*(1-aa[...,None])
im=Image.fromarray(np.clip(out,0,255).astype(np.uint8)).convert('RGBA'); d=ImageDraw.Draw(im)
T(345,1450,'1 kg',XB(120),anchor='ms'); T(345,1540,'$12.000',XB(70),anchor='ms')
T(825,1450,'1/2 kg',XB(120),anchor='ms'); T(825,1540,'$8.000',XB(70),anchor='ms')
d.line((80,1650,1000,1650),fill='#FFFFFF',width=3)
T(80,1712,'Pedí por mensaje y te la llevamos.',RG(36),stroke=False)
LG=r'C:\Users\Lauti\Documents\Proyecto - Achilata\06_Assets\logo\achilata-sin-bajada-blanco.png'
lg=Image.open(LG).convert('RGBA'); lg=lg.crop(lg.getbbox()); lw=190; lg=lg.resize((lw,round(lg.height*lw/lg.width)),Image.LANCZOS)
im.alpha_composite(lg,(1000-lw,1712-lg.height+8))
im.convert('RGB').save(OUT)
