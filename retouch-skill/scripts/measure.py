"""Measure a BG-swap output against BG_Ref: wall colour (outside the subject) and wall/floor seam height.
Prints which fallback is needed. usage: measure.py bgswap.png bg_ref.png  [wall_tol=6] [seam_tol=0.02]"""
import sys, numpy as np
from PIL import Image
from rembg import remove, new_session
p, refp = sys.argv[1:3]
WT = float(sys.argv[3]) if len(sys.argv) > 3 else 6; ST = float(sys.argv[4]) if len(sys.argv) > 4 else 0.02
def seam(a):
    col = a[:, 20:80].mean(1); ys = np.where(col[:, 0] - col[:, 2] > 12)[0]
    return ys[0] / a.shape[0] if len(ys) else None
ref = np.asarray(Image.open(refp).convert('RGB')).astype(float); rs = seam(ref)
REFWALL = np.median(ref[:int(ref.shape[0] * rs * 0.85)].reshape(-1, 3), 0)
img = Image.open(p).convert('RGB'); o = np.asarray(img).astype(float)
bg = np.asarray(remove(img, session=new_session('isnet-general-use'), only_mask=True)) < 10
floor = (o[:, :, 0] - o[:, :, 2] > 12) & (o.mean(2) < 225)
wall = np.median(o[bg & ~floor], 0); s = seam(o)
need = []
if np.abs(wall - REFWALL).max() > WT: need.append('A')
if s is None or abs(s - rs) > ST: need.append('B')
print(f'wall {wall.round().astype(int).tolist()} (ref {REFWALL.round().astype(int).tolist()})  '
      f'seam {None if s is None else round(s*100,1)}% (ref {round(rs*100,1)}%)  fix: {"+".join(need) or "none"}')
