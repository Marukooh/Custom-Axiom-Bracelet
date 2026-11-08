# Nexus Mods page setup (manual, one-off)

**Main file ID:** 8344104 (set as `NEXUSMODS_FILE_ID` in the GitHub environment `nexusmods` on 2026-11-08;
`NEXUSMODS_API_KEY` set by Marco the same day). Mod page ID: not recorded yet.

Nexus has no API to create a mod page: it is created once on the website, then every update goes
through the **Release** GitHub workflow.

## Page fields
- **Name:** `Custom Axiom Bracelet`
- **Summary:** `nexusmods/short-description.txt`
- **Description:** `nexusmods/full-description.bbcode.txt` (BBCode editor)
- **Category:** Cheats and God items (or Gameplay)
- **Tags:** Cheating, Gameplay, Quality of Life, Items, Overpowered
- **Version:** `2.04.08` (mod version = game version it is validated for, like the author's other mods)
- **Main image (thumbnail):** `art/thumbnail.png` (1280×720); also add `art/banner.png`
- **Requirements:** Definitive Mod Manager (mod 633); notes: "4.8 or newer. Linux/Steam Deck: winmm=n,b".
  Optional DLC: Charting the Unknown (Underwater card only)
- **Permissions:** no re-upload, no modification, no asset use, no conversion, no use in other mods
  or mod packs; credit: "See NOTICE.md on GitHub"; donation points as preferred
- **Source code link:** https://github.com/Marukooh/Custom-Axiom-Bracelet

## First file
Run `python3 build.py`, then upload `release/Custom Axiom Bracelet v2.04.08.zip` as a **Main** file
named `Custom Axiom Bracelet`, with "Mod Manager Download" enabled.

## Link the workflow
1. Read the **file ID** of the file you just uploaded (Nexus "Manage files", in the file's edit link).
2. GitHub → repo Settings → Environments → create `nexusmods`:
   - secret `NEXUSMODS_API_KEY` = your personal Nexus API key (nexusmods.com → Site preferences → API Keys);
   - variable `NEXUSMODS_FILE_ID` = the file ID above.
3. From then on: set `VERSION` in `build.py` to the new game version (or add a letter, `2.04.08b`, for a
   second release on the same game version), commit, push, then Actions → **Release** → Run workflow
   (version, changelog, "publish_nexus").
