# Feed completo 26/11/2026 · reels R03 La textura, R01 Una cucharada y R07 Te la llevamos.
# Se renderizan cuadro por cuadro a 30 fps y se codifican con ffmpeg. Sin audio: el audio se elige en Instagram.
# Uso: python build_feed_reels.py <carpeta de recortes V>
from feed_comun import *
import subprocess
V=sys.argv[1]; FPS=30; W,H=S
BB={}
def colocar(L,n,sc,px,py,ref='cb'):
    F,a=cut(V,n)
    ys,xs=np.where(a>0.5); x0,y0,x1,y1=xs.min(),ys.min(),xs.max(),ys.max()
    rx={'c':(x0+x1)/2,'l':x0,'r':x1}[ref[0]]; ry={'b':y1,'t':y0,'c':(y0+y1)/2}[ref[1]]
    return L.poner(F,a,sc,round(px-rx*sc),round(py-ry*sc))
def estudio(n,sc,px,py,ref,sombra,seed):
    L=Lienzo(W,H,seed=seed); A=colocar(L,n,sc,px,py,ref)
    if sombra=='piso': L.sombra_piso(A,py)
    elif sombra=='aire': L.sombra_aire(A,dx=30,dy=44,blur=34,fuerza=0.30)
    return L.render(None,None).convert('RGB')
def liso(seed=9):
    return Lienzo(W,H,seed=seed).render(None,None).convert('RGB')

ease=lambda t:1-(1-min(max(t,0),1))**3
def zoom(img,z,cx=0.5,cy=0.5):
    if abs(z-1)<1e-3: return img.copy()
    cw,ch=W/z,H/z; x0=(W-cw)*cx; y0=(H-ch)*cy
    return img.resize((W,H),Image.BICUBIC,box=(x0,y0,x0+cw,y0+ch))
def texto(frame,items,t):
    """items: (t0, x, y, texto, fuente, anchor, trazo, tipo). Entra subiendo 36 px y apareciendo en 0,3 s."""
    for t0,x,y,s,f,an,st,kind in items:
        if t<t0: continue
        k=ease((t-t0)/0.3)
        lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
        if kind=='pills': numeros(d,x,y+round(36*(1-k)))
        elif kind=='logo':
            lg=logo(f); lay.alpha_composite(lg,(round(x-lg.width/2),round(y-lg.height+36*(1-k))))
        else: T(d,x,y+round(36*(1-k)),s,f,anchor=an,stroke=st)
        if k<1:
            a=lay.getchannel('A').point(lambda v:int(v*k)); lay.putalpha(a)
        frame.paste(lay,(0,0),lay)
    return frame

def codificar(escenas,salida,portada_t=None):
    """escenas: lista de (duración, función(tiempo local) -> imagen RGB)"""
    os.makedirs(os.path.dirname(salida),exist_ok=True)
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',salida],stdin=subprocess.PIPE)
    for dur,fn in escenas:
        for i in range(round(dur*FPS)):
            p.stdin.write(np.asarray(fn(i/FPS)).tobytes())
    p.stdin.close(); p.wait()

def carpeta(n): d=f'{C}\\Reels\\{n}\\final'; os.makedirs(d,exist_ok=True); return d
CIERRE_Y=1180
def cierre(t,titulo,seed=9,base=None):
    fr=(base or liso(seed)).copy()
    return texto(fr,[(0.0,540,760,titulo,fit(titulo,900,mx=170),'ms',True,'t'),
                     (0.25,0,0,None,380,None,None,'logo') if False else (0.25,540,1000,None,380,None,None,'logo'),
                     (0.5,540,1090,'Helado tucumano en Salta.',RG(44),'ms',False,'t'),
                     (0.75,197,CIERRE_Y,None,None,None,None,'pills')],t)

# ================= R03 · La textura =================
d=carpeta('R03 La textura')
M=[macro('04',W,H,0.5,0.1,1.7,0.06,301),macro('22',W,H,0.5,0.4,3.0,0.06,302),
   macro('22',W,H,0.35,0.45,3.5,0.06,303),macro('22',W,H,0.55,0.42,3.8,0.06,304).transpose(Image.FLIP_LEFT_RIGHT)]
M=[m.convert('RGB') for m in M]
txt=['Mirá esta textura.','Hielo raspado.','Color fucsia.','Receta tucumana.']
fin=liso(305)
def esc(i):
    return lambda t:texto(zoom(M[i],1+0.05*t/2.4),[(0.15,80,1470 if i==0 else 1010,txt[i],fit(txt[i],900,mx=150),'ls',True,'t')],t)
escenas=[(2.4,esc(i)) for i in range(4)]+[(2.6,lambda t:cierre(t,'Hay achilata.',base=fin))]
codificar(escenas,f'{d}\\R03 la textura.mp4')
fc=fit('Mirá esta',900,mx=260); texto(M[1].copy(),[(-1,80,1010,'Mirá esta',fc,'ls',True,'t'),(-1,80,1010+round(fc.size*0.92),'textura.',fc,'ls',True,'t')],1).save(f'{d}\R03 portada.png')

# ================= R01 · Una cucharada =================
d=carpeta('R01 Una cucharada')
cortes=[('16',0.78,1080,1460,'rb','piso',311),('14',0.78,0,1920+20,'lb','',312),('02',0.80,1080,1920,'rb','',313),
        ('07',0.85,0,1560,'lb','piso',314),('13',0.80,1080,1920,'rb','',315),('10',0.85,540,1920+40,'cb','',316)]
E=[estudio(*c) for c in cortes]
fin=estudio('28',0.78,540,1500,'cb','piso',317)
def esc(i):
    def f(t):
        fr=zoom(E[i],1.06-0.06*ease(t/0.35))
        f=fit('Una cucharada',920,mx=170); g=round(f.size*0.95)
        its=[(-1,80,470,'Una cucharada',f,'ls',True,'t')]
        if i>=3: its.append((-1 if i>3 else 0.0,80,470+g,'y estás en',f,'ls',True,'t'))
        if i>=4: its.append((-1 if i>4 else 0.0,80,470+2*g,'Tucumán.',f,'ls',True,'t'))
        return texto(fr,its,t)
    return f
def primera(t):
    fr=zoom(E[0],1.06-0.06*ease(t/0.35))
    return texto(fr,[(0.2,80,470,'Una cucharada',fit('Una cucharada',920,mx=170),'ls',True,'t')],t)
def final(t):
    fr=fin.copy()
    return texto(fr,[(0.0,80,470,'Pedí la tuya.',fit('Pedí la tuya.',920,mx=170),'ls',True,'t'),
                     (0.2,82,560,'1 kg a $12.000 y medio kilo a $8.000.',RG(42),'ls',False,'t'),
                     (0.4,80,620,None,None,None,None,'pills')],t)
escenas=[(1.4,primera)]+[(0.9,esc(i)) for i in range(1,6)]+[(2.8,final)]
codificar(escenas,f'{d}\\R01 una cucharada.mp4')
f=fit('Una cucharada',920,mx=170); g=round(f.size*0.95); texto(E[0].copy(),[(-1,80,470,'Una cucharada',f,'ls',True,'t'),(-1,80,470+g,'y estás en',f,'ls',True,'t'),(-1,80,470+2*g,'Tucumán.',f,'ls',True,'t')],1).save(f'{d}\R01 portada.png')

# ================= R07 · Te la llevamos =================
d=carpeta('R07 Te la llevamos')
base=estudio('05',1.02,1080,860,'rt','aire',321)
zonas=[['Grand Bourg.'],['San Lorenzo.'],['San Lorenzo','Chico.'],['El Tipal.'],['La Almudena.']]
FZ0=fit('San Lorenzo.',920,mx=230); FZ=lambda z:FZ0
def lineas(ls,t0): return [(t0,78,640+j*round(FZ0.size*0.92),l,FZ0,'ls',True,'t') for j,l in enumerate(ls)]
def zona(i):
    def f(t):
        fr=zoom(base,1.0+0.012*(i+t/1.3),0.7,0.6)
        return texto(fr,[(-1,82,420,'Te la llevamos a',RG(52),'ls',False,'t')]+lineas(zonas[i],0.0),t)
    return f
def otra(t):
    fr=zoom(base,1.07,0.7,0.6)
    return texto(fr,[(-1,82,420,'Y si estás en otra zona,',RG(52),'ls',False,'t'),(0.0,78,640,'consultanos.',FZ('consultanos.'),'ls',True,'t')],t)
fin=liso(322)
escenas=[(1.6,zona(0))]+[(1.3,zona(i)) for i in range(1,5)]+[(1.8,otra),(2.8,lambda t:cierre(t,'Pedí la tuya.',base=fin))]
codificar(escenas,f'{d}\\R07 te la llevamos.mp4')
texto(base.copy(),[(-1,82,420,'Te la llevamos a',RG(52),'ls',False,'t'),(-1,78,600,'tu casa.',fit('tu casa.',900,mx=260),'ls',True,'t')],1).save(f'{d}\\R07 portada.png')
print('ok')
