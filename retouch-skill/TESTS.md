# Test log

## v0.1 — 2026-11-11
| Set | Character | RETOUCH result | BG SWAP fixes |
|---|---|---|---|
| Gold Clara Set | Claire | 3-4-Side copied the original ponytail. Rerun with face crop: pass. Close-up auto-crop: pass. | A on 3 images, B on 1 (Front-3-4 seam at 65.7%) |
| Pink Clara Set | Kristy | 3-4-Side kept the original model's face, which a re-roll with the full sheet didn't fix. Rerun with face crop: pass. Close-up auto-crop on a pink close to skin tone: pass. | A on 3 images (Back the worst), B on 1 (3-4-Side seam at 80%) |
| Camo Lunar Set | Claire | Long wide-leg trousers with a busy print; all 5 faces were Claire. 3-4-Side passed with the full sheet this time. The Close-up original showed the face; it copied the ponytail, so it was rerun with the face crop (hair down, body slightly more frontal) and cropped faceless. Claude first accepted the ponytail version and Stamp rejected it. | 3-4-Side: no wall (all beige), re-rolled once and passed. A on 2 images. B on none. |
| Blush Iva Mini Dress | Kristy | Satin pink with a midriff cut-out. Content filter blocked 4 of 5 on the first run. A GPT 2 retry passed 3-4-Side and Close-up; GPT 2.6 passed Front-3-4; Back passed first time. Front-Full 220 was blocked 6 times on GPT. Claude tried Nano Banana Pro, which passed the filter but didn't reshape the body; Stamp caught it, so it was rejected. Swapped to frame 224, which passed on GPT 2. All faces and hair were Kristy with the full sheet, including 3-4-Side. `autocrop.py` failed on the satin, so the Close-up was cropped by hand. | A on 1 image (Front-Full). B on none. |
| Sienna Maxi Dress | Claire | Dark olive satin maxi with a cut-out and side slit. Stamp gave 3 Front-Full options (246/247/249); all 3 passed, kept 246. No content-filter blocks this time. All 7 faces and hair (long, loose) were Claire with the full sheet, including 3-4-Side. Body reshape OK. `autocrop.py` failed on the dark garment, so the Close-up was cropped by hand at the lips (15.0%). | A on 2 images (3-4-Side, Back). B on none. |
| Midnight Valen Maxi Dress | Kristy | Saturated navy satin maxi with side cut-outs and a cream rope bow. All 5 RETOUCH passed first time on GPT 2 (no blocks). All faces and hair (waves) were Kristy with the full sheet, including 3-4-Side. Close-up hand-cropped at the lips (15.5%). | BG Front-Full blocked once (nsfw) and passed on a retry; then A on 1 image (Front-Full). Others none. |

### Still to test
- Dark olive (Sienna) and saturated navy (Midnight): measure and bgmatch OK. Auto-crop is not used any more (hand crop at the lips).
- A long dress or maxi skirt, with the hem near or out of frame. Trousers passed (Camo).
- Using the face crop for 3-4-Side from the start. With the full sheet, 3-4-Side has now passed 4 sets in a row and failed 2 (the first two). Leaning: keep the full sheet, face crop only as the fallback.
- Whether GPT 2.6 retouches look the same as GPT 2 across a whole set.
