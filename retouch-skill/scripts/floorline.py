"""Move the wall/floor seam of a flat-studio BG-swap image to the same height as in BG_Ref (83.5% for the current BG_Ref).
Wall below the old seam = wall colour from just above it; floor = BG_Ref floor texture. Subject composited back on top.
usage: floorline.py in.png bg_ref.png out.png [target_fraction]"""
import sys, numpy as np
from PIL import Image, ImageFilter
from rembg import remove, new_session
src, refp, dst = sys.argv[1:4]; T = float(sys.argv[4]) if len(sys.argv) > 4 else None
img = Image.open(src).convert('RGB'); o = np.asarray(img).astype(float); H, W, _ = o.shape
col = o[:, 20:80].mean(1); s = int(np.where(col[:, 0] - col[:, 2] > 12)[0][0])
ref = np.asarray(Image.open(refp).convert('RGB')); rh = ref.shape[0]
rs = int(np.where(ref[:, :, 0].astype(int) - ref[:, :, 2] > 12)[0][0])
if T is None: T = rs / rh          # default: same beige height as BG_Ref
t = int(T * H)
bg = o.copy()
wall = np.median(np.concatenate([o[s-80:s-25, :150], o[s-80:s-25, -150:]], 1).reshape(-1, 3), 0)
bg[min(s, t)-12:t] = wall if t > s else bg[min(s,t)-12:t]
floor = Image.fromarray(ref[rs + 2:]).resize((W, H - t))
bg[t:] = np.asarray(floor).astype(float)
m = remove(img, session=new_session('isnet-general-use'), only_mask=True).filter(ImageFilter.GaussianBlur(1.2))
a = (np.asarray(m).astype(float) / 255)[..., None]
Image.fromarray(np.clip(o * a + bg * (1 - a), 0, 255).astype('uint8')).save(dst)
print(f'seam {s/H:.3f} -> {T}')
