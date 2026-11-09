#!/usr/bin/env python3
"""Build "Custom Axiom Bracelet": ONE zip holding one DMM pack per buff group, one tickable member per buff.

Input: the Axiom Bracelet buff table further down (EDITIONS).
Output: release/Custom Axiom Bracelet <N> - <Group>/ (dmm_pack.json + one folder per option) and one zip with all of them.

DMM has no author-defined sub-groups inside a pack card, so each group is its own pack: one import,
one collapsible card per group. The Axiom Bracelet's buff, stat and passive lists are empty in vanilla
2.04.08, so each entry is its own `list_append` member and the options stack. Member titles start with
their position so they sort the same whatever DMM sorts by.
"""
import json
import shutil
import zipfile
from pathlib import Path

VERSION = "2.04.08b"  # mod version = game version it is validated for (2.04.08b for a second release)
GAME = "2.04.08"
NAME = "Custom Axiom Bracelet"
AUTHOR = "Marukooh"
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "release"

BANDS = [("Daeil_Band", 1001129), ("OOngka_Daeil_Band", 1002864), ("Damian_Daeil_Band", 1003248)]
EB = "enchant_data_list[0].equip_buffs"
ST = "enchant_data_list[0].enchant_stat_data.stat_list_static"
SL = "enchant_data_list[0].enchant_stat_data.stat_list_static_level"
PS = "equip_passive_skill_list"
ABYSS = " Counts as 1 Abyss effect."
DLC = " Requires the Charting the Unknown DLC."
NEW = " Highest level the game defines."

GROUPS = {  # group -> pack description
    "Combat": "Attack, defense, attack speed, critical rate and healing on hit for the Axiom Bracelet.",
    "Resistances": "Fire, ice, lightning and fall damage protection for the Axiom Bracelet.",
    "Regeneration": "HP, Spirit and Stamina regeneration and lower stamina use for the Axiom Bracelet.",
    "Movement": "Move, climb and swim speed for the Axiom Bracelet.",
    "Underwater (DLC)": "Breath buffs for the Axiom Bracelet. Requires the Charting the Unknown DLC.",
    "Utility": "Thievery, animal friendship, contribution EXP and two passive skills for the Axiom Bracelet.",
}

# (group, label, field, element, description, needs_dlc)
# Names from buffinfo / statusinfo / skill in 2.04.08 (DDD = attack damage, DPV = defense).
# Extra buffs use the max level the buff record defines (u32 @+21); 1000333/1000334/1000352 exist
# only in buffinfo.dlc_01.
BRACELET = [
    ("Combat", "Attack +999", ST, {"stat": 1000002, "change_mb": 999000},
     "Attack damage (DDD stat) +999.", False),
    ("Combat", "Defense +999", ST, {"stat": 1000003, "change_mb": 999000},
     "Defense (DPV stat) +999.", False),
    ("Combat", "Attack Speed Lv15", SL, {"stat": 1000010, "change_mb": 15}, "Attack speed level 15.", False),
    ("Combat", "Critical Rate Lv15", SL, {"stat": 1000007, "change_mb": 15}, "Critical hit rate level 15.",
     False),
    ("Combat", "Heal on Hit Lv10", EB, {"buff": 1000252, "level": 10}, "Recover HP when you hit." + ABYSS,
     False),
    ("Resistances", "Fire Resistance Lv15", EB, {"buff": 1000012, "level": 15},
     "Resist fire and heat." + ABYSS, False),
    ("Resistances", "Ice Resistance Lv15", EB, {"buff": 1000013, "level": 15},
     "Resist ice and cold." + ABYSS, False),
    ("Resistances", "Lightning Resistance Lv15", EB, {"buff": 1000014, "level": 15},
     "Resist lightning." + ABYSS, False),
    ("Resistances", "Fall Damage Reduction Lv10", EB, {"buff": 1000185, "level": 10},
     "Take less damage from falls." + ABYSS, False),
    ("Regeneration", "HP Regen Lv50", EB, {"buff": 1000008, "level": 50}, "HP regeneration." + ABYSS, False),
    ("Regeneration", "Spirit Regen Lv50", EB, {"buff": 1000009, "level": 50},
     "Spirit (MP) regeneration." + ABYSS, False),
    ("Regeneration", "Stamina Regen Lv50", EB, {"buff": 1000046, "level": 50},
     "Stamina regeneration." + ABYSS, False),
    ("Regeneration", "Lower Stamina Use Lv10", EB, {"buff": 1000015, "level": 10},
     "Actions use less stamina." + ABYSS, False),
    ("Movement", "Move Speed Lv15", SL, {"stat": 1000011, "change_mb": 15}, "Movement speed level 15.", False),
    ("Movement", "Climb Speed Lv15", EB, {"buff": 1000100, "level": 15}, "Climb faster." + ABYSS, False),
    ("Movement", "Swim Speed Lv10", EB, {"buff": 1000107, "level": 10}, "Swim faster." + NEW + ABYSS,
     False),
    ("Underwater (DLC)", "Max Breath Lv80", EB, {"buff": 1000333, "level": 80},
     "Stay underwater much longer." + NEW + DLC + ABYSS, True),
    ("Underwater (DLC)", "Breath Regen Lv5", EB, {"buff": 1000334, "level": 5},
     "Breath refills faster." + NEW + DLC + ABYSS, True),
    ("Underwater (DLC)", "Breath on Hit Lv3", EB, {"buff": 1000352, "level": 3},
     "Recover breath when you hit." + NEW + DLC + ABYSS, True),
    ("Utility", "Thievery Lv15", EB, {"buff": 1000119, "level": 15}, "Better at stealing." + ABYSS, False),
    ("Utility", "Animal Friendship Lv15", EB, {"buff": 1000124, "level": 15},
     "Animals befriend you faster." + ABYSS, False),
    ("Utility", "Contribution EXP Lv15", EB, {"buff": 1000114, "level": 15},
     "More contribution experience." + ABYSS, False),
    ("Utility", "Metal Magnet (passive)", PS, {"skill": 75047, "level": 1},
     "Passive skill Passive_Item_MagnetMetal: pulls in metal items.", False),
    ("Utility", "Restriction Immunity (passive)", PS, {"skill": 70994, "level": 1},
     "Passive skill Equip_Passive_RestrictionImmune: immune to movement-blocking effects.", False),
]


def mod_json(title, desc, intents, dlc=False):
    m = {
        "modinfo": {"title": title, "version": VERSION, "author": AUTHOR, "description": desc},
        "format": 3, "format_minor": 1,
        "targets": [{"file": "iteminfo.pabgb", "intents": intents}],
    }
    if dlc:
        m["requires_dlc"] = True
    return m


def safe(s):
    return "".join(c if c.isalnum() or c in " -+" else "_" for c in s).strip()


def build():
    options = {g: [] for g in GROUPS}  # group -> [(label, desc, intents, dlc)]
    for group, label, field, elem, desc, dlc in BRACELET:
        rows = [{"entry": e, "key": k, "field": field, "op": "list_append", "new": elem} for e, k in BANDS]
        options[group].append((label, desc + " Axiom Bracelet of Kliff, Oongka and Damiane.", rows, dlc))

    for old in OUT.glob(f"{NAME}*"):
        shutil.rmtree(old) if old.is_dir() else old.unlink()
    packs = []
    for gi, (group, gdesc) in enumerate(GROUPS.items(), 1):
        pack = OUT / f"{NAME} {gi} - {safe(group)}"
        pack.mkdir(parents=True)
        packs.append(pack)
        (pack / "dmm_pack.json").write_text(json.dumps({
            "title": f"{NAME} {gi} - {group}", "version": VERSION, "author": AUTHOR,
            "description": f"{gdesc} Part of Custom Axiom Bracelet for game {GAME}, one tickable option per buff.",
        }, indent=1), encoding="utf-8")
        for n, (label, desc, rows, dlc) in enumerate(options[group], 1):
            title = f"{n}. {label}"
            d = pack / safe(title)
            d.mkdir()
            (d / f"{safe(title)}.json").write_text(json.dumps(mod_json(title, desc, rows, dlc), indent=1),
                                                   encoding="utf-8")

    zpath = OUT / f"{NAME} v{VERSION}.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for pack in packs:
            for f in sorted(pack.rglob("*")):
                if f.is_file():
                    z.write(f, f.relative_to(OUT))
    return options, packs, zpath


if __name__ == "__main__":
    opts, packs, z = build()
    for pack in packs:
        print(pack.name)
        for d in sorted(p.name for p in pack.iterdir() if p.is_dir()):
            print("   ", d)
    print(z)
