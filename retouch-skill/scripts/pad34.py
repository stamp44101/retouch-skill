"""Pad a 2:3 retouch to 3:4 with flat backdrop-coloured side strips (subject scale and position unchanged).
usage: pad34.py in.png out.png"""
import sys, numpy as np
from PIL import Image
im = Image.open(sys.argv[1]).convert('RGB'); w, h = im.size
W = round(h * 3 / 4); pad = (W - w) // 2; a = np.asarray(im)
L = np.median(a[:, :10], axis=1).astype('uint8'); R = np.median(a[:, -10:], axis=1).astype('uint8')
out = np.zeros((h, W, 3), 'uint8'); out[:, :pad] = L[:, None]; out[:, pad + w:] = R[:, None]; out[:, pad:pad + w] = a
Image.fromarray(out).save(sys.argv[2]); print(f'{w}x{h} -> {W}x{h}')
