# Un solo fucsia para toda la achilata · 26/11/2026
# Lauti quiere que el helado de todas las fotos tenga el fucsia chillón de la foto 05,
# el de H09 envíos zonas y P13 1. Se cambia solo el helado: ni el logo rojo de los potes, ni el fondo, ni las manos.
# Método de editor:
#  1. se detecta el helado por color, rosa o rojo saturado, y se quedan solo las manchas grandes, así las letras del logo no entran;
#  2. la máscara se suaviza para que no haya corte entre lo corregido y lo que no;
#  3. en LAB se llevan la media y el desvío del helado a los del helado de la foto 05.
#     La luz, la sombra y la textura de cada foto se conservan; cambia el tono.
import numpy as np,cv2
# fucsia de la foto 05, medido en el helado puro, LAB de OpenCV: media y desvío
OBJETIVO=(np.array([116.3,193.0,150.3],np.float32),np.array([35.3,16.1,9.2],np.float32))

def mascara_helado(rgb,alpha=None):
    u8=np.clip(rgb,0,255).astype(np.uint8)
    hsv=cv2.cvtColor(u8,cv2.COLOR_RGB2HSV)
    h,s,v=hsv[...,0].astype(int),hsv[...,1].astype(int),hsv[...,2].astype(int)
    A_=cv2.cvtColor(u8,cv2.COLOR_RGB2LAB)[...,1].astype(int)
    cand=((h>=158)|(h<=6))&(s>140)&(v>55)&(A_>172)   # rosa o rojo muy saturado; el a alto de LAB deja afuera la piel, aunque el fondo rojo la tiña
    if alpha is not None: cand&=alpha>0.5
    cerr=cv2.morphologyEx(cand.astype(np.uint8),cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))
    # una apertura grande borra los trazos finos de las letras del logo y deja solo las manchas del helado
    k=max(21,int(0.035*min(rgb.shape[:2])))
    ab=cv2.morphologyEx(cerr,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(k,k)))
    n,lab,st,_=cv2.connectedComponentsWithStats(ab,8)
    areas=st[1:,cv2.CC_STAT_AREA] if n>1 else np.array([0])
    # la a del logo con su gota, las uñas y las yemas de los dedos quedan afuera: chicas en sí y al lado de la bocha más grande
    keep=np.zeros(n,bool); keep[1:]=(areas>0.005*ab.size)&(areas>0.10*areas.max())
    nucleo=keep[lab].astype(np.uint8)
    # el helado se reconstruye alrededor de esas manchas, con su borde real; las letras quedan lejos y no entran
    cerca=cv2.dilate(nucleo,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(k+10,k+10)))
    m=(cerr*cerca).astype(np.float32)
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15)))
    # se rellenan los huecos chicos de adentro, las sombras profundas del helado, para que todo quede del mismo tono
    cs,_=cv2.findContours((m>0.5).astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    lleno=np.zeros(m.shape,np.uint8); cv2.drawContours(lleno,cs,-1,1,-1)
    m=np.maximum(m,lleno.astype(np.float32))
    m=cv2.GaussianBlur(m,(0,0),2.2)
    if alpha is not None: m*=np.clip(alpha,0,1)
    return np.clip(m,0,1)

def stats(rgb,m):
    lab=cv2.cvtColor(np.clip(rgb,0,255).astype(np.uint8),cv2.COLOR_RGB2LAB).astype(np.float32)
    w=m>0.9
    return lab[w].mean(0),lab[w].std(0)+1e-3

def al_fucsia(rgb,mu_t,sd_t,alpha=None,fuerza=1.0):
    m=mascara_helado(rgb,alpha)
    if m.max()<0.5: return rgb,m
    mu,sd=stats(rgb,m)
    lab=cv2.cvtColor(np.clip(rgb,0,255).astype(np.uint8),cv2.COLOR_RGB2LAB).astype(np.float32)
    out=lab.copy()
    # L: se lleva la media y se conserva casi todo el contraste propio, para no aplanar la textura
    kL=np.clip(sd_t[0]/sd[0],0.85,1.2)
    out[...,0]=(lab[...,0]-mu[0])*kL+mu_t[0]
    for c in (1,2): out[...,c]=(lab[...,c]-mu[c])*(sd_t[c]/sd[c])+mu_t[c]
    res=cv2.cvtColor(np.clip(out,0,255).astype(np.uint8),cv2.COLOR_LAB2RGB).astype(np.float32)
    k=(m*fuerza)[...,None]
    return rgb*(1-k)+res*k,m
