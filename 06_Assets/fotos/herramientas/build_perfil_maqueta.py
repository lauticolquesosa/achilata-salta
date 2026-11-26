# Maqueta del perfil completo y foto de perfil · 26/11/2026
from feed_comun import *
OUT=C+r'\Perfil completo'; os.makedirs(OUT,exist_ok=True)
PU=C+r'\Publicaciones'; RE=C+r'\Reels'; DE=C+r'\Destacadas'

# foto de perfil: logo principal rojo sobre blanco, más grande para que se lea en el círculo chico
lg=Image.open(RAIZ+r'\06_Assets\logo\achilata-principal-rojo.png').convert('RGBA'); lg=lg.crop(lg.getbbox())
w=round(1080*0.80); lg=lg.resize((w,round(lg.height*w/lg.width)),Image.LANCZOS)
fp=Image.new('RGBA',(1080,1080),'white'); fp.alpha_composite(lg,((1080-lg.width)//2,(1080-lg.height)//2+20))
fp.convert('RGB').save(OUT+r'\foto de perfil 1080.png')

# la grilla, de la más nueva arriba a la izquierda
G=[[(PU,'P12 Achilata en tu fiesta','P12 1 en tu fiesta.png'),(PU,'P11 Te la llevamos','P11 portada.png'),(PU,'P10 La achilata anotada','P10 1 anotada.png')],
   [(PU,'P09 No deslices','P09 1 no deslices.png'),(PU,'P08 Etiquetá a quien le debés','P08 1 etiqueta.png'),(PU,'P07 Una cucharada','P07 portada.png')],
   [(PU,'P06 Cómo pedir','P06 1 portada.png'),(PU,'P05 Hace 32 grados','P05 1 hace 32.png'),(PU,'P04 La textura','P04 portada.png')],
   [(PU,'P03 Achilata, sustantivo','P03 1 achilata.png'),(PU,'P02 El menú','P02 1 el menu.png'),(PU,'P01 Hay achilata en Salta','P01 1 portada.png')]]
cw=360; ch=480; gap=4
W=3*cw+2*gap; top=800
M=Image.new('RGB',(W,top+4*(ch+gap)),'#0C1014'); d=ImageDraw.Draw(M)
# encabezado
pf=fp.resize((220,220),Image.LANCZOS); mk=Image.new('L',(220,220),0); ImageDraw.Draw(mk).ellipse((0,0,219,219),fill=255)
M.paste(pf,(40,60),mk)
d.text((300,80),'achilatasalta',font=RG(44),fill='white')
for i,(n,l) in enumerate([('12','publicaciones'),('549','seguidores'),('2','seguidos')]):
    d.text((300+i*250,160),n,font=XB(40),fill='white'); d.text((300+i*250,210),l,font=RG(28),fill='#ddd')
d.text((40,310),'Achilata Salta',font=XB(32),fill='white')
for i,s in enumerate(['Helado tucumano en Salta 🍧'.replace(' 🍧',''),'Potes y carrito para eventos','Envíos a San Lorenzo, El Tipal, Grand Bourg y más','Pedí al 387 483 4041 o 387 468 4498','achilata-salta.vercel.app']):
    d.text((40,356+i*40),s,font=RG(28),fill='#8fb4ff' if i==4 else 'white')
# destacadas
for i,(f,t) in enumerate([('portada 1 menu.png','Menú'),('portada 2 pedidos.png','Pedidos'),('portada 3 zonas.png','Zonas'),('portada 4 eventos.png','Eventos'),('portada 5 achilata.png','Achilata')]):
    im=Image.open(f'{DE}\\{f}').crop((90,450,990,1350)).resize((150,150),Image.LANCZOS)
    x=40+i*210; y=570
    d.ellipse((x-6,y-6,x+156,y+156),outline='#555',width=3)
    mk=Image.new('L',(150,150),0); ImageDraw.Draw(mk).ellipse((0,0,149,149),fill=255); M.paste(im,(x,y),mk)
    d.text((x+75,y+200),t,font=RG(26),fill='white',anchor='ms')
for r,fila in enumerate(G):
    for c,(base,carp,f) in enumerate(fila):
        im=Image.open(f'{base}\\{carp}\\final\\{f}').convert('RGB')
        w,h=im.size; th=w*4/3
        if th>h: nw=h*3/4; im=im.crop(((w-nw)/2,0,(w+nw)/2,h))
        else: im=im.crop((0,(h-th)/2,w,(h+th)/2))
        M.paste(im.resize((cw,ch),Image.LANCZOS),(c*(cw+gap),top+r*(ch+gap)))
M.save(OUT+r'\maqueta del perfil.png')
print('ok')
