# Retouch skill (v0.1)

A Claude skill for SHER product shots. It takes the original studio photos of a dress and does two things:
1. **RETOUCH:** puts one of the KOL characters on them, using GPT Image 2.
2. **BG SWAP:** moves them onto the brand backdrop at 3:4, using Nano Banana Pro.

Both checkpoints were moved from Figma Weave to the Higgsfield MCP. The prompts are kept word for word.

> **v0.1:** tested on 2 sets (Gold Clara × Claire, Pink Clara × Kristy). See "Known gaps" in `SKILL.md`.

## Install
- **Quickest:** add `retouch-skill/SKILL.md` as a skill in Claude. It is self-contained: the scripts are in its appendix.
- **Full:** download this repo (Code → Download ZIP) and install the `retouch-skill` folder.

## Before you start
1. Connect the **Higgsfield** connector in Claude with the SHER Higgsfield account.
2. Set Claude's network access to **All domains**.
3. The fallback scripts need `rembg`. The first run downloads a model of about 179 MB.

## Use
Say: "รีทัช [dress name] ด้วย [character]" and give the folder of originals plus `BG_Ref.png`.

You get:
- `02_READY`: the retouches (2:3)
- `04_BG`: the finals on the brand backdrop (3:4)
- `03_Review`: contact sheets for checking

## Files
- `retouch-skill/SKILL.md`: the skill (source of truth)
- `retouch-skill/scripts/`:
  - `pad34.py`: pads a retouch to 3:4 before BG SWAP
  - `autocrop.py`: crops the Close-up back to the original framing
  - `measure.py`: measures wall colour and floor line after BG SWAP
  - `bgmatch.py`: fallback A, fixes backdrop colour
  - `floorline.py`: fallback B, fixes the floor line
- `retouch-skill/TESTS.md`: test log
