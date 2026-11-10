"""Shift the backdrop (wall + floor) of a BG-swap output to the BG_Ref colours. Subject untouched (rembg mask).
usage: bgmatch.py bgswap_output.png bg_ref.png out.png"""
import sys, numpy as np
from PIL import Image, ImageFilter
from rembg import remove, new_session
out_p, ref_p, dst = sys.argv[1:4]
ref=np.asarray(Image.open(ref_p).convert('RGB')).astype(float); h=ref.shape[0]
WALL=np.median(ref[:int(h*.7)].reshape(-1,3),0); FLOOR=np.median(ref[int(h*.9):].reshape(-1,3),0)
img=Image.open(out_p).convert('RGB'); o=np.asarray(img).astype(float)
sub=remove(img, session=new_session('isnet-general-use'), only_mask=True)
sub=sub.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(4))   # grow subject a little, soft edge
bg=1-np.asarray(sub).astype(float)/255
floor=(o[:,:,0]-o[:,:,2]>12)&(o.mean(2)<225)
hard=bg>0.95
off=np.zeros_like(o)
off[~floor]=WALL-np.median(o[hard&~floor],0)
if (hard&floor).sum()>1000: off[floor]=FLOOR-np.median(o[hard&floor],0)
Image.fromarray(np.clip(o+off*bg[...,None],0,255).astype('uint8')).save(dst)
print(dst,'wall shift',(WALL-np.median(o[hard&~floor],0)).round())
