# Nexus Mods page setup (manual, one-off)

**Main file ID:** 8344104 (set as `NEXUSMODS_FILE_ID` in the GitHub environment `nexusmods` on 2026-11-08;
`NEXUSMODS_API_KEY` still to be set by Marco). Mod page ID: not recorded yet.

Nexus has no API to create a mod page: it is created once on the website, then every update goes
through the **Deploy to Nexus Mods** GitHub workflow.

## Page fields
- **Name:** `Custom Axiom Bracelet`
- **Summary:** `nexusmods/short-description.txt`
- **Description:** `nexusmods/full-description.bbcode.txt` (BBCode editor)
- **Category:** Cheats and God items (or Gameplay)
- **Tags:** Cheating, Gameplay, Quality of Life, Items, Overpowered
- **Version:** `1.2.0`
- **Main image (thumbnail):** `art/thumbnail.png` (1280×720); also add `art/banner.png`
- **Requirements:** Definitive Mod Manager (mod 633); notes: "4.8 or newer. Linux/Steam Deck: winmm=n,b".
  Optional DLC: Charting the Unknown (Underwater card only)
- **Permissions:** no re-upload, no modification, no asset use, no conversion, no use in other mods
  or mod packs; credit: "See NOTICE.md on GitHub"; donation points as preferred
- **Source code link:** https://github.com/Marukooh/Custom-Axiom-Bracelet

## First file
Run `python3 build.py`, then upload `release/Custom Axiom Bracelet v1.2.0.zip` as a **Main** file
named `Custom Axiom Bracelet`, with "Mod Manager Download" enabled.

## Link the workflow
1. Read the **file ID** of the file you just uploaded (Nexus "Manage files", in the file's edit link).
2. GitHub → repo Settings → Environments → create `nexusmods`:
   - secret `NEXUSMODS_API_KEY` = your personal Nexus API key (nexusmods.com → Site preferences → API Keys);
   - variable `NEXUSMODS_FILE_ID` = the file ID above.
3. From then on: bump `VERSION` in `build.py`, commit, push, then Actions → **Deploy to Nexus Mods** →
   Run workflow with the same version.
