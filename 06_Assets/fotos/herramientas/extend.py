import cv2, numpy as np
def extend(img, mask_ex, X, T, B, Xr=None, grain=1.6, seed=7):
    """img float HxWx3, mask_ex bool (product+shadow to ignore). Pads left X, right Xr, top T, bottom B."""
    Xr = X if Xr is None else Xr
    H,W,_=img.shape
    s=4; sm=cv2.resize(img,(W//s,H//s),interpolation=cv2.INTER_AREA)
    mm=cv2.resize(mask_ex.astype(np.uint8),(W//s,H//s),interpolation=cv2.INTER_NEAREST)
    fill=cv2.inpaint(np.clip(sm,0,255).astype(np.uint8),mm*255,15,cv2.INPAINT_TELEA).astype(np.float32)
    fill=cv2.GaussianBlur(fill,(0,0),6)
    pad=cv2.copyMakeBorder(fill,T//s,B//s,X//s,Xr//s,cv2.BORDER_REPLICATE)
    # progressively smooth outward so replicated streaks dissolve
    inner=np.zeros(pad.shape[:2],np.float32); inner[T//s:T//s+H//s,X//s:X//s+W//s]=1
    dist=cv2.distanceTransform((1-inner).astype(np.uint8),cv2.DIST_L2,5)
    acc=pad.copy()
    for sig in [4,8,16,32]:
        b=cv2.GaussianBlur(pad,(0,0),sig); w=np.clip(dist/(sig*2.0),0,1)[...,None]
        acc=acc*(1-w)+b*w
    Hc,Wc=H+T+B,W+X+Xr
    low=cv2.resize(acc,(Wc,Hc),interpolation=cv2.INTER_CUBIC)
    rng=np.random.default_rng(seed)
    n=cv2.GaussianBlur(rng.normal(0,1,(Hc,Wc)).astype(np.float32),(0,0),0.7); n/=n.std()
    canvas=low+n[...,None]*grain
    a=np.zeros((Hc,Wc),np.float32); a[T:T+H,X:X+W]=1
    a=cv2.GaussianBlur(cv2.erode(a,np.ones((31,31),np.uint8)),(0,0),5)
    big=canvas.copy(); big[T:T+H,X:X+W]=img
    return np.clip(big*a[...,None]+canvas*(1-a[...,None]),0,255).astype(np.uint8)
