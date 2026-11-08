# Custom Axiom Bracelet

![Custom Axiom Bracelet](art/banner.png)

A Crimson Desert mod for [Definitive Mod Manager](https://www.nexusmods.com/crimsondesert/mods/633) (DMM) that lets you
choose, one by one, the buffs on the Axiom Bracelet (Kliff, Oongka and Damiane), plus a few Quality of Life changes.

- Game version: **2.04.08**
- DMM: 4.8 or newer (format 3 field edits, so it survives most game updates)

## What you get

One zip with seven DMM cards. Every row is an independent checkbox:

| Card | Options |
|---|---|
| 1 - Combat | Attack +999, Defense +999, Attack Speed, Critical Rate, Heal on Hit |
| 2 - Resistances | Fire, Ice, Lightning, Fall Damage Reduction |
| 3 - Regeneration | HP, Spirit, Stamina, Lower Stamina Use |
| 4 - Movement | Move, Climb, Swim Speed |
| 5 - Underwater (DLC) | Max Breath, Breath Regen, Breath on Hit (needs Charting the Unknown) |
| 6 - Utility | Thievery, Animal Friendship, Contribution EXP, Metal Magnet, Restriction Immunity |
| 7 - Quality of Life | Max Stack 999999, 99 Charges, Shorter Item Cooldowns, Durability 65535, Never Destroyed When Broken |

Each bracelet buff counts as one Abyss effect.

## Install

1. In DMM press Import and pick the zip.
2. Tick the options you want, then Mount.

Linux / Steam Deck: the Steam launch options need `WINEDLLOVERRIDES="winmm=n,b" %command%`.

## Build

```bash
python3 build.py
```

Writes the seven pack folders and `release/Custom Axiom Bracelet v<VERSION>.zip`. Python 3 standard library only.

## Release

The `Deploy to Nexus Mods` workflow builds the zip and uploads it as a new version of an existing Nexus file.
It needs the repository secret `NEXUSMODS_API_KEY`, the variable `NEXUSMODS_FILE_ID` and an environment
called `nexusmods`. Bump `VERSION` in `build.py`, then run the workflow with the same version.

## License

Source-available, all rights reserved: see [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md). Contributions are welcome.
