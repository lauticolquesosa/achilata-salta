import sys,os,numpy as np,cv2
sys.path.insert(0,sys.argv[2]); from studio import *
from PIL import ImageDraw,ImageFont
V=sys.argv[1]; O=V+'/out'
FD=r'C:\Users\Lauti\AppData\Local\Microsoft\Windows\Fonts'
def XB(s): return ImageFont.truetype(FD+r'\BricolageGrotesque-ExtraBold.ttf',s)
def RG(s): return ImageFont.truetype(FD+r'\BricolageGrotesque-Regular.ttf',s)
def INK(s): return ImageFont.truetype(r'C:\Windows\Fonts\Inkfree.ttf',s)
W_='#FFFFFF'; ROJ='#E7364A'
LG=r'C:\Users\Lauti\Documents\Proyecto - Achilata\06_Assets\logo'
def logo(w,color='blanco'):
    im=Image.open(os.path.join(LG,f'achilata-sin-bajada-{color}.png')).convert('RGBA'); im=im.crop(im.getbbox())
    return im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
cache={}
def src(n,flip=False):
    im=np.asarray(Image.open(f'{V}/src{n}.png').convert('RGB')).astype(np.float32); a=np.load(f'{V}/a{n}.npy')
    if n in ('02','13'):
        L=cv2.cvtColor(im.astype(np.uint8),cv2.COLOR_RGB2LAB).astype(np.float32)
        yel=np.clip((L[...,2]-140)/12,0,1)*np.clip((142-L[...,1])/8,0,1)
        L[...,1]=L[...,1]+yel*(L[...,2]-128)*0.9
        L[...,2]=L[...,2]-yel*(L[...,2]-128)*0.85
        im=cv2.cvtColor(np.clip(L,0,255).astype(np.uint8),cv2.COLOR_LAB2RGB).astype(np.float32)
    if flip: im=im[:,::-1].copy(); a=a[:,::-1].copy()
    return im,a
def frame(n,box,size,flip=False,gamma=1.0):
    """box=(x0,y0,x1,y1) in source px, may exceed bounds -> background extended. returns bg, fg, alpha at final size"""
    im,a=src(n,flip); H,W=a.shape; x0,y0,x1,y1=box
    T,B,L,R=max(0,-y0),max(0,y1-H),max(0,-x0),max(0,x1-W)
    bg,F,A=studio(im,a,T,B,L,R,gamma=gamma)
    cx0,cy0=x0+L,y0+T
    sl=(slice(cy0,cy0+(y1-y0)),slice(cx0,cx0+(x1-x0)))
    rs=lambda z:cv2.resize(z[sl],size,interpolation=cv2.INTER_AREA if (x1-x0)>size[0] else cv2.INTER_LANCZOS4)
    return rs(bg),rs(F),np.clip(rs(A),0,1)
def tlines(d,x,top,lines,font,fill,lh,stroke=True,align='left',W=1080):
    sw=max(2,round(font.size*0.03)) if stroke else 0
    asc=font.getbbox('H')[1]
    for i,t in enumerate(lines):
        xx=x
        if align=='center': xx=(W-d.textlength(t,font=font))/2
        d.text((xx,top-asc+i*lh),t,font=font,fill=fill,stroke_width=sw,stroke_fill=fill)
def compose(bg,F,A,text_fn=None,front_fn=None):
    """text_fn draws text BEHIND subject; front_fn draws over everything"""
    base=Image.fromarray(bg.astype(np.uint8)).convert('RGBA')
    if text_fn: text_fn(ImageDraw.Draw(base),base)
    b=np.asarray(base.convert('RGB')).astype(np.float32)
    out=F*A[...,None]+b*(1-A[...,None])
    img=Image.fromarray(np.clip(out,0,255).astype(np.uint8)).convert('RGBA')
    if front_fn: front_fn(ImageDraw.Draw(img),img)
    return img.convert('RGB')
P=(1080,1350); S=(1080,1920)
# ---------- P01 ----------
bg,F,A=frame('05',(0,60,1024,1340),P)
def t(d,im): tlines(d,80,190,['Hay achilata','en Salta.'],XB(150),W_,142)
def f(d,im): lg=logo(200); im.alpha_composite(lg,(80,1350-80-lg.height))
compose(bg,F,A,t,f).save(f'{O}/P01 1 portada.png')
bg,F,A=frame('16',(0,-420,1254,1147),P,gamma=0.55)
def t(d,im):
    tlines(d,80,110,['Dicen que','los vendedores','gritaban','hay gelata.'],XB(86),W_,84)
def f(d,im):
    fi=INK(48); d.text((80,452),'y de tanto escucharlo quedó achilata.',font=fi,fill=W_)
compose(bg,F,A,t,f).save(f'{O}/P01 2 el nombre.png')
bg,F,A=frame('10',(240,420,840,1170),P)
def f(d,im): tlines(d,80,1350-100-2*64-50,['Hielo raspado.','Color fucsia.','Receta tucumana.'],XB(60),W_,64)
compose(bg,F,A,None,f).save(f'{O}/P01 3 textura.png')
bg,F,A=frame('11',(-145,-335,1256,1415),P)
def t(d,im): tlines(d,80,110,['Potes de 1 kg','y medio kilo.'],XB(108),W_,103)
compose(bg,F,A,t,None).save(f'{O}/P01 4 potes.png')
im=Image.new('RGB',P,ROJ).convert('RGBA'); d=ImageDraw.Draw(im)
lg=logo(640); im.alpha_composite(lg,((1080-640)//2,250))
tlines(d,80,600,['Pedidos por','WhatsApp.'],XB(96),W_,92)
tlines(d,80,830,['387 483 4041','387 468 4498'],XB(64),W_,74)
tlines(d,80,1060,['Delivery en Grand Bourg, San Lorenzo Chico,','San Lorenzo, El Tipal y La Almudena.','Transferencia o efectivo.'],RG(34),W_,46,stroke=False)
im.convert('RGB').save(f'{O}/P01 5 pedidos.png')
# ---------- H01 ----------
bg,F,A=frame('02',(0,-284,1024,1536),S)
def t(d,im): tlines(d,0,330,['Volvimos.'],XB(186),W_,180,align='center')
def f(d,im): lg=logo(240); im.alpha_composite(lg,((1080-240)//2,250))
compose(bg,F,A,t,None).save(f'{O}/H01 1 volvimos 19.30.png')
im=Image.new('RGB',S,ROJ).convert('RGBA'); d=ImageDraw.Draw(im)
tlines(d,0,300,['Nueva','publicación.'],XB(120),W_,114,align='center')
d.text(((1080-d.textlength('deslizá hasta el final',font=INK(56)))/2,1560),'deslizá hasta el final',font=INK(56),fill=W_)
lg=logo(220); im.alpha_composite(lg,((1080-220)//2,1670-lg.height+10))
im.convert('RGB').save(f'{O}/H01 2 nueva publicacion 20.05.png')
bg,F,A=frame('07',(0,-300,1089,1636),S,gamma=0.38)
def f(d,im):
    tlines(d,80,300,['1 kg  $12.000'],XB(104),W_,100)
    tlines(d,80,440,['Medio kilo  $8.000'],XB(84),W_,90)
    tlines(d,80,1560,['Delivery en zonas seleccionadas.','Pedidos por WhatsApp.'],RG(40),W_,52,stroke=False)
compose(bg,F,A,None,f).save(f'{O}/H01 3 precios 20.30.png')
bg,F,A=frame('13',(0,-450,900,1150),S,flip=True)
def t(d,im): tlines(d,80,300,['¿Ya probaste','achilata?'],XB(128),W_,122)
compose(bg,F,A,t,None).save(f'{O}/H01 4 encuesta 21.00.png')
im=Image.new('RGB',S,ROJ).convert('RGBA'); d=ImageDraw.Draw(im)
tlines(d,80,300,['Pedidos por','WhatsApp.'],XB(120),W_,114)
tlines(d,80,580,['387 483 4041','387 468 4498'],XB(84),W_,96)
tlines(d,80,1300,['Delivery en Grand Bourg,','San Lorenzo Chico, San Lorenzo,','El Tipal y La Almudena.','Otras zonas, consultanos.'],RG(40),W_,54,stroke=False)
lg=logo(240); im.alpha_composite(lg,(80,1670-lg.height))
im.convert('RGB').save(f'{O}/H01 5 pedidos 22.00.png')
# sheets
import glob
fs=sorted(glob.glob(f'{O}/P01 *.png')); s=Image.new('RGB',(5*432+60,560),'#777')
for i,p in enumerate(fs): s.paste(Image.open(p).resize((432,540)),(10+i*442,10))
s.save(f'{V}/sheetP.jpg',quality=88)
fs=sorted(glob.glob(f'{O}/H01 *.png')); s=Image.new('RGB',(5*360+60,660),'#777')
for i,p in enumerate(fs): s.paste(Image.open(p).resize((360,640)),(10+i*370,10))
s.save(f'{V}/sheetH.jpg',quality=88)
