# Test log

## v0.1 — 2026-11-11
| Set | Character | RETOUCH result | BG SWAP fixes |
|---|---|---|---|
| Gold Clara Set | Claire | 3-4-Side copied the original ponytail. Rerun with face crop: pass. Close-up auto-crop: pass. | A on 3 images, B on 1 (Front-3-4 seam at 65.7%) |
| Pink Clara Set | Kristy | 3-4-Side kept the original model's face, which a re-roll with the full sheet didn't fix. Rerun with face crop: pass. Close-up auto-crop on a pink close to skin tone: pass. | A on 3 images (Back the worst), B on 1 (3-4-Side seam at 80%) |
| Camo Lunar Set | Claire | Long wide-leg trousers with a busy print; all 5 faces were Claire. 3-4-Side passed with the full sheet this time. The Close-up original showed the face; it copied the ponytail, so it was rerun with the face crop (hair down, body slightly more frontal) and cropped faceless. Claude first accepted the ponytail version and Stamp rejected it. | 3-4-Side: no wall (all beige), re-rolled once and passed. A on 2 images. B on none. |

### Still to test
- A dark or saturated garment: auto-crop and seam detection.
- A long dress or maxi skirt, with the hem near or out of frame. Trousers passed (Camo).
- Using the face crop for 3-4-Side from the start.
