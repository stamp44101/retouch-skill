---
name: retouch-skill
description: SHER product-shot pipeline on Higgsfield. RETOUCH puts a KOL character on the original studio shots (GPT Image 2). BG SWAP moves them onto the brand backdrop at 3:4 (Nano Banana Pro). Use for "retouch", "รีทัช", "เปลี่ยน BG", or a dress folder plus a character.
version: 0.1
---

# Retouch skill — v0.1

> **v0.1:** tested on 2 sets only: Gold Clara Set × Claire and Pink Clara Set × Kristy, 5 angles each. See "Known gaps" before trusting a run without looking at it.

Pipeline: preflight → intake → **Checkpoint 1 RETOUCH** → QA → **Checkpoint 2 BG SWAP** → measure → fallbacks (only when needed) → deliver to folders.
Everything needed is in this file; the scripts are in the appendix. Reply in the user's language (casual Thai by default) with English technical terms. Show images, keep text short.

## Fixed vs adaptable
- **Fixed (never change):**
  - both prompts, word for word, even a typo;
  - models, resolution and aspect;
  - media order;
  - the floor-line rule;
  - the folder layout and file naming.
- **Adaptable:** how files get in and out (device folder, Drive, chat upload), and how the scripts are run.
- **Fix outputs with code, never by editing the prompt.** The prompts have worked for a long time in Figma Weave; when an output is off, fix it in a script before or after generation.

## Step 0 — Preflight
1. Higgsfield MCP tools: `generate_image_batch`, `generate_image`, `jobs_wait`, `media_upload`, `media_confirm`. Load them with tool search if they are deferred. If they are missing, tell the user to connect the Higgsfield connector, and stop.
2. The sandbox must reach `upload.higgsfield.ai` and `d8j0ntlcm91z4.cloudfront.net`, for the curl PUT upload and the result downloads.
3. Install `pip install "rembg[cpu]"`. The first run downloads the `isnet-general-use` model, about 179 MB, from github.com. Only the fallback scripts need it.
4. Credits:
   - RETOUCH: 2 credits per image at 2k.
   - BG SWAP: Nano Banana Pro at 2k; check the cost with `get_cost`.
   - A 5-angle set usually needs 1–2 reruns as well.

## Step 1 — Intake
| Needed | Notes |
|---|---|
| Folder of original studio shots for one dress | usually 5 angles |
| Dress name | used in file names, e.g. `Pink-Clara-Set` |
| Character | one of the current cast. Image 2 = that character's **Character Sheet V2** image, the source image of her Soul/Element in HF. Ask if not given; if the user says "pick", choose one who has worn fewer sets |
| BG_Ref.png | the brand backdrop: white wall + beige floor |

Name each original's angle by looking at it:
- `Front-Full`: full body, front
- `Front-3-4`: front, cropped around the knees
- `3-4-Side`: body turned to the side
- `Close-up`: head cut off at the frame top
- `Back`: back view

## Checkpoint 1 — RETOUCH
Settings:
- Model: `gpt_image_2`, quality `medium`, resolution `2k`, aspect `2:3`. Output is 1360x2048. `1k` gives 688x1024 and drifts more.
- Medias, both with role `image`, in this order: [original shot, character sheet].
- Run all angles in one `generate_image_batch`.

Prompt (verbatim):
```
<Role & Objective>
You are a retoucher who works in 'High-End Beauty' for a fashion label. Edit ONE photograph to show the character at the brand's beauty standard, without distorting the garment.
</Role & Objective>

<Input>
Image 1: ORIGINAL — Garment & Camera Shot truth
Image 2: CHARACTER  — Person truth: only face, hair, and skin
</Input>

<character — Head>
Replace the face, hair, and skin with those of the person in Image 2, then groom for the shoot.
- Makeup: skin glowing, brows neat, lashes defined, lips with sheen.
- Hair: glossy and professionally styled.
</character — Head>

<character — Body>
Reshaped to the beauty standard below. Extra length in the legs and the neck. Waist narrow and high, limbs slim.
Positions are measured from the top of the head in head-lengths. If feet is not shown, imagine where it would be instead of trying to enforce the positions.
- Upper: mid-bust at 2, natural waist at 3
- Lower: widest hip at 3.5, crotch at 4.2, mid-thigh at 5, knee at 6, floor at 9
- Arms: elbow at 3, wrist at 4, fingertips at 4.75
Widths are measured in multiples of head-widths.
- Upper: shoulder at 1.5, waist at 0.6
- Lower: each thigh at 0.15, hips at 1.6
</character — Body>


<Do's>
- Reproduce the garment exactly as it appears in Image 1.
- Keep the pose and Camera Shot from Image 1.
- Zoom in if necessary to maintain the Camera Shot if it is a 3/4 Body or Close-up.
- The garment sits on the body with natural weight: slight creasing and fold where fabric meets the figure. It is worn, not floating.
</Do's>

<Don't>
- No stretched or warped garment where the Body was reshaped
- No deviation from the Camera Angle from Image 1
- No over-smoothed skin, no distorted proportions.
</Don't>

<Output>
ONE photograph. Maximum resolution.
</Output>
```

### Close-up: auto-crop (always)
The original cuts the head off, but the prompt needs the head: for the face swap, and because the body is measured in head-lengths from the top of the head. So the model zooms out to show the face.

Fix: run `autocrop.py original.jpg retouch.png out.png`. It aligns the garment's top edge (neckline) and bottom edge (hem) with the original, at the original's aspect ratio. Keep the uncropped render in `99_Test`.

### QA after RETOUCH (Claude looks, then the user approves)
1. **Face.** Zoom into every face and compare it with the sheet. The face must be the character, not the original model. This is the most common failure, and it is easy to miss on a small contact sheet.
2. **Hair.** The model can copy the original's hairstyle, e.g. a ponytail.
3. **Garment:** pattern, neckline and hem match the original. **Shoes** match the original.
4. **Framing** matches the original; for the Close-up, after the auto-crop.

### Fallback: wrong face or hair (note, watching)
Rerun only that angle, with Image 2 = a crop of the sheet's top-left close-up face panel (about x 0–29.8%, y 0–44.5% of the sheet).
- **3-4-Side failed with the full sheet in both test sets** (ponytail copied in one, original face kept in the other). A re-roll with the full sheet failed again; the face crop passed both times.
- **Open decision:** use the face crop for 3-4-Side from the start. Not decided yet.

Save the passing shots to `02_READY`. Save a contact sheet to `03_Review`: originals on the top row, retouches below.

## Checkpoint 2 — BG SWAP
1. **Pad first (always).** Run `pad34.py retouch.png padded.png`. It adds flat backdrop-coloured strips to the left and right so the 2:3 retouch becomes 3:4. Without this, the model zooms out to fill 3:4 and the subject shrinks.
2. Settings:
   - Model: `nano_banana_pro`, resolution `2k`, aspect `3:4`. Output is 1792x2400. HF's job list labels it `nano_banana_2`; the HF page shows Pro.
   - Medias, both with role `image_references`, in this order: [padded retouch, BG_Ref].

Prompt (verbatim):
```
<role>
Background replacer. You repaint the pixels behind the subject. You do not re-stage the shot.
</role>

<input>
Image 1: PHOTO — the base photograph being edited. Subject truth, framing truth: pose, crop, scale, camera distance, aspect ratio.
Image 2: BACKDROP — style reference for the new background only: color, texture, material, lighting quality. Ignore its scale, depth, framing, and camera distance completely.
</input>

<method>
This is a masked background swap, not a composite. The subject's pixels stay exactly where they are — same position in frame, same size in pixels, same crop at every edge. Only the area behind the subject changes.
Never place the subject into the BACKDROP's space. The BACKDROP supplies surface and light, nothing else.
</method>

<framing — locked>
Output matches the PHOTO's aspect ratio, crop, and subject scale exactly. The subject fills the same proportion of the frame as it does in the PHOTO.
If the PHOTO is a 3/4 body or close-up, the output stays a 3/4 body or close-up. Never widen out. Never add space above the head, below the crop line, or to the sides.
Where the subject meets a frame edge, it runs out of frame — the frame cuts through it.
</framing — locked>

<do>
- Repaint the background in the BACKDROP's color, texture, and lighting character.
- Keep the subject's pose, body, garment, hair, and edges untouched.
- Match the light direction already on the subject so the new backdrop reads as the same room.
</do>

<don't>
- No cast shadow behind the subject
- No shortened, stretched, or restyled physique
- No change to subject scale, crop, or aspect ratio
- No scale or depth borrowed from the BACKDROP image
</don't>

<output>
ONE photograph. Maximum resolution.
</output>
```

### House rule: floor line
The beige floor band has the **same height in every angle, Close-up included**. That height is set by BG_Ref: the seam sits at 83.5% of frame height.

### Measure every output, then fix only what is off
Run `measure.py bgswap.png BG_Ref.png` on every output. It prints the wall colour, the seam height and the fix needed:
- **A: wall colour off** (more than 6 levels in any channel). Run `bgmatch.py`. It shifts the wall and floor colours to BG_Ref, outside the subject only, using a rembg mask.
- **B: seam off** (more than ±2% of frame height). Run `floorline.py`. It repaints the wall and floor so the seam sits at BG_Ref's height, then puts the subject back on top.
- Keep the raw output of any fixed image in `99_Test/bg-raw`.
- Add a row to the log: set, angle, wall, seam, fix.

So far: A was needed on 5 of 10 images and B on 2 of 10, so expect both to come up in most sets.

## Deliver
```
RETOUCH\[Dress-Name]\
  01_Original\   originals
  02_READY\      [Dress]_[Character]_[Angle].png      (retouch, 2:3)
  03_Review\     contact sheets, BG-check, retake checks
  04_BG\         [Dress]_[Character]_[Angle]_BG.png   (final, 3:4)
  99_Test\       rejects, alternates, uncropped, bg-raw
```
End with one line per angle (pass, or what was fixed) and the credits used.

## Known gaps (v0.1)
- Not tested yet on dark or saturated garments, or on long dresses and skirts. `autocrop.py` and the seam detection may fail on those; check those outputs by eye.
- `bgmatch.py` and `floorline.py` only work on a flat studio backdrop of two colours, like BG_Ref.
- Face QA still needs human eyes.
- The scripts are separate, not one runner yet.

## Appendix — scripts
The same files are in `scripts/`.

### `pad34.py`
```python
"""Pad a 2:3 retouch to 3:4 with flat backdrop-coloured side strips (subject scale and position unchanged).
usage: pad34.py in.png out.png"""
import sys, numpy as np
from PIL import Image
im = Image.open(sys.argv[1]).convert('RGB'); w, h = im.size
W = round(h * 3 / 4); pad = (W - w) // 2; a = np.asarray(im)
L = np.median(a[:, :10], axis=1).astype('uint8'); R = np.median(a[:, -10:], axis=1).astype('uint8')
out = np.zeros((h, W, 3), 'uint8'); out[:, :pad] = L[:, None]; out[:, pad + w:] = R[:, None]; out[:, pad:pad + w] = a
Image.fromarray(out).save(sys.argv[2]); print(f'{w}x{h} -> {W}x{h}')
```

### `autocrop.py`
```python
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
```

### `measure.py`
```python
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
```

### `bgmatch.py`
```python
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
```

### `floorline.py`
```python
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
```
