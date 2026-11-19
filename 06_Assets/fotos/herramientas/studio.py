import cv2, numpy as np
from PIL import Image
ROJO=np.array([0xE7,0x36,0x4A],np.float32)
def lab(im): return cv2.cvtColor(np.clip(im,0,255).astype(np.uint8),cv2.COLOR_RGB2LAB).astype(np.float32)
def make_alpha(im, rb, bright=True, chroma=True, lo=7, hi=14, minarea=3000, extra=None):
    L=lab(im); H,W=L.shape[:2]
    border=np.concatenate([L[:8].reshape(-1,3),L[-8:].reshape(-1,3),L[:,:8].reshape(-1,3),L[:,-8:].reshape(-1,3)])
    ref=np.median(border,0)
    # local bg estimate: big blur of image with subject removed via rembg
    k=np.zeros((H,W),np.float32)
    if bright: k=np.maximum(k,np.clip((L[...,0]-ref[0]-lo)/(hi-lo),0,1))
    if chroma:
        d=np.sqrt(((L[...,1:]-ref[1:])**2).sum(-1)); k=np.maximum(k,np.clip((d-lo)/(hi-lo),0,1))
    a=np.maximum(k,rb)
    if extra is not None: a=np.maximum(a,extra)
    hard=(a>0.5).astype(np.uint8)
    n,lb,st,_=cv2.connectedComponentsWithStats(hard)
    keep=np.zeros_like(hard)
    for i in range(1,n):
        if st[i,4]>minarea: keep[lb==i]=1
    ff=keep.copy(); m2=np.zeros((H+2,W+2),np.uint8)
    # fill small holes only
    inv=(1-keep).astype(np.uint8); n2,lb2,st2,_=cv2.connectedComponentsWithStats(inv)
    for i in range(1,n2):
        if st2[i,4]<4000: keep[lb2==i]=1
    alpha=np.clip(a,0,1)*cv2.dilate(keep,np.ones((3,3),np.uint8))
    alpha=np.maximum(alpha,cv2.erode(keep,np.ones((5,5),np.uint8)).astype(np.float32))
    return cv2.GaussianBlur(alpha,(0,0),0.7), ref
def bg_lum(im, alpha):
    """luminance of the background with the subject inpainted, real shadows kept"""
    H,W=alpha.shape; s=4
    L=lab(im)[...,0]
    sm=cv2.resize(L,(W//s,H//s),interpolation=cv2.INTER_AREA)
    mk=cv2.resize((alpha>0.1).astype(np.uint8),(W//s,H//s),interpolation=cv2.INTER_NEAREST)
    mk=cv2.dilate(mk,np.ones((5,5),np.uint8))
    f=cv2.inpaint(np.clip(sm,0,255).astype(np.uint8),mk*255,9,cv2.INPAINT_TELEA).astype(np.float32)
    f=cv2.GaussianBlur(f,(0,0),1.5)
    return cv2.resize(f,(W,H),interpolation=cv2.INTER_CUBIC)
def pad(arr,T,B,Lf,R):
    s=4; H,W=arr.shape[:2]
    sm=cv2.resize(arr,(W//s,H//s),interpolation=cv2.INTER_AREA)
    p=cv2.copyMakeBorder(sm,T//s,B//s,Lf//s,R//s,cv2.BORDER_REPLICATE)
    inner=np.zeros(p.shape[:2],np.float32); inner[T//s:T//s+H//s,Lf//s:Lf//s+W//s]=1
    dist=cv2.distanceTransform((1-inner).astype(np.uint8),cv2.DIST_L2,5)
    acc=p.copy()
    for sig in [4,8,16,32]:
        b=cv2.GaussianBlur(p,(0,0),sig); w=np.clip(dist/(sig*2.0),0,1)
        if acc.ndim==3: w=w[...,None]
        acc=acc*(1-w)+b*w
    out=cv2.resize(acc,(W+Lf+R,H+T+B),interpolation=cv2.INTER_CUBIC)
    out[T:T+H,Lf:Lf+W]=arr
    return out
def studio(im, alpha, T=0,B=0,Lf=0,R=0, gamma=1.0, color=ROJO, grain=1.4, seed=1, ref_pct=90, Fo=None):
    lum=bg_lum(im,alpha)
    ref=np.percentile(lum[alpha<0.05],ref_pct)
    ratio=np.clip(lum/ref,0.25,1.25)**gamma
    # decontaminate subject edges against original bg
    H,W=alpha.shape
    Lorig=lab(im)
    bgcol=cv2.GaussianBlur(np.where(alpha[...,None]<0.05,im,0),(0,0),8)/np.maximum(cv2.GaussianBlur((alpha<0.05).astype(np.float32),(0,0),8)[...,None],1e-3)
    A=alpha[...,None]
    F=np.clip((im-(1-A)*bgcol)/np.maximum(A,0.2),0,255)
    F=np.where(A>0.97,im,F)
    if Fo is not None: F=Fo
    if T or B or Lf or R:
        ratio=pad(ratio,T,B,Lf,R); F=pad(F,T,B,Lf,R) ; alpha=pad(alpha,T,B,Lf,R)
        Hn,Wn=alpha.shape; z=np.zeros((Hn,Wn),np.float32); z[T:T+H,Lf:Lf+W]=1
        alpha=alpha*z; 
    Hn,Wn=alpha.shape
    rng=np.random.default_rng(seed); g=cv2.GaussianBlur(rng.normal(0,1,(Hn,Wn)).astype(np.float32),(0,0),0.7); g/=g.std()
    bg=color[None,None,:]*ratio[...,None]+g[...,None]*grain
    return np.clip(bg,0,255), np.clip(F,0,255), np.clip(alpha,0,1)
