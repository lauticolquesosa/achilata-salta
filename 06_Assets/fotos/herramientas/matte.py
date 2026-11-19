import sys,time,cv2,numpy as np
from PIL import Image
def box(x,r): return cv2.boxFilter(x,-1,(2*r+1,2*r+1),normalize=True,borderType=cv2.BORDER_REFLECT)
def guided_color(I,p,r,eps):
    mI=[box(I[...,c],r) for c in range(3)]; mp=box(p,r)
    cov=[box(I[...,c]*p,r)-mI[c]*mp for c in range(3)]
    var=np.zeros(I.shape[:2]+(3,3),np.float32)
    for i in range(3):
        for j in range(3):
            var[...,i,j]=box(I[...,i]*I[...,j],r)-mI[i]*mI[j]+(eps if i==j else 0)
    inv=np.linalg.inv(var.reshape(-1,3,3)).reshape(var.shape)
    c=np.stack(cov,-1)
    a=np.einsum('...ij,...j->...i',inv,c)
    b=mp-sum(a[...,k]*mI[k] for k in range(3))
    ma=np.stack([box(a[...,k],r) for k in range(3)],-1); mb=box(b,r)
    return (ma*I).sum(-1)+mb
def blur_fusion(I,a,r):
    a3=a[...,None]
    def once(F,B,r):
        bl=lambda x:cv2.blur(x,(r,r))
        ba=bl(a)[...,None]; bna=bl(1-a)[...,None]
        Fb=bl(F*a3)/np.maximum(ba,1e-5); Bb=bl(B*(1-a3))/np.maximum(bna,1e-5)
        res=I-a3*Fb-(1-a3)*Bb
        return np.clip(Fb+a3*res,0,1),np.clip(Bb+(1-a3)*res,0,1)
    F,B=once(I,I,r); F,B=once(F,B,6)
    return F
V=sys.argv[1]
for n in sys.argv[2:]:
    t=time.time()
    I=np.asarray(Image.open(f'{V}/src{n}.png').convert('RGB')).astype(np.float32)/255
    A0=np.load(f'{V}/a{n}_orig.npy') if __import__('os').path.exists(f'{V}/a{n}_orig.npy') else np.load(f'{V}/a{n}.npy')
    np.save(f'{V}/a{n}_orig.npy',A0)
    hard=(A0>0.5).astype(np.uint8)
    hard=cv2.morphologyEx(hard,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))
    hard=cv2.morphologyEx(hard,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
    k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9))
    fg=cv2.erode(hard,k); bgm=1-cv2.dilate(hard,k)
    g=guided_color(I,hard.astype(np.float32),4,1e-4)
    a=np.clip(g,0,1); a[fg>0]=1; a[bgm>0]=0
    a=np.clip((a-0.06)/0.88,0,1)
    F=blur_fusion(I,a,91)
    np.save(f'{V}/a{n}.npy',a.astype(np.float32)); np.save(f'{V}/f{n}.npy',(F*255).astype(np.float32))
    print(n,round(time.time()-t,1),'s')
