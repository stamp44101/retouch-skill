"""Auto-crop a retouched shot back to the original's framing (used for Close-up).
Anchors: garment top edge (neckline) and garment bottom edge (hem), found as where the
centre band switches between saturated skin and low-saturation fabric.
usage: autocrop.py original.jpg retouched.png out.png
"""
import sys, numpy as np
from PIL import Image

def anchors(img, n=300):
    im = img.convert('RGB')
    a = np.asarray(im.resize((200, n))).astype(float)[:, 80:120]
    sat = ((a.max(2) - a.min(2)) / np.maximum(a.max(2), 1)).mean(1)
    k = 5; sat = np.convolve(sat, np.ones(k)/k, mode='same')
    fab = sat < 0.08
    run = 6
    top = next(y for y in range(n - run) if fab[y:y+run].all())
    hem = next((y for y in range(n - run, top, -1) if fab[y-run:y].all() and not fab[y:y+run].any()), None)
    return top / n, (hem / n if hem else None)

o = Image.open(sys.argv[1]); r = Image.open(sys.argv[2])
ot, oh = anchors(o); rt, rh = anchors(r)
W, H = r.size
s = (rh - rt) / (oh - ot) if (oh and rh) else 1.0   # crop height as fraction of retouched height
s = min(1.0, s)
ch = int(H * s); cw = int(ch * o.width / o.height)
if cw > W: cw = W; ch = int(cw * o.height / o.width)
top = int(round(rt * H - ot * ch)); top = max(0, min(H - ch, top))
left = (W - cw) // 2
print(f'orig top/hem {ot:.3f}/{oh}  retouched {rt:.3f}/{rh}  crop {cw}x{ch} @ {left},{top}')
r.crop((left, top, left + cw, top + ch)).save(sys.argv[3])
