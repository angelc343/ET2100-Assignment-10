# Elden Ring: Shattered Grace

A complete, turn-based terminal RPG inspired by Elden Ring. This version updates the original project with visible connected maps, animated effects, reliable quest progression, and recoverable defeats. No game assets or official game code are included.

## Start on your Mac

1. Unzip this folder.
2. Open Terminal in `elden_ring_terminal_rpg` (or open the folder in VS Code and use Terminal → New Terminal).
3. Install both required libraries:

   ```bash
   uv add colorama tinydb
   ```

4. Run:

   ```bash
   uv run main.py
   ```

If you use Python without uv:

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

Choose **2** to register, then **1** to log in. Password characters do not appear as you type; press Enter when finished. Use a normal Terminal window, not an IDE Output panel. A window about 80 columns wide and 30 rows high works well. All commands use **a key followed by Enter**, including the effects demo. Movement is turn-based, not real-time.

## Exploration controls

| Command | Action |
| --- | --- |
| W / A / S / D | Move north / west / south / east |
| T | Talk on or next to an NPC |
| J | View main quest, shard count, and side quests |
| I | View inventory |
| U | Use an item or equip an owned weapon |
| C | View level, HP, XP, gold, equipment, skills, and quest stage |
| K | Shop while next to Merchant Kale |
| G | Restore HP and reset cooldowns while standing on a golden `*` |
| V | Open the effects demonstration |
| P | Save immediately |
| X | Save and return to the title flow |
| Ctrl+C | Leave gameplay and save; at the title, exit |

The map appears immediately after login and again every exploration turn. `@` is you, `#` is a wall, `~` is impassable water, `!` is an undefeated enemy, `D` is the final boss, and `*` is a Site of Grace. NPCs have cyan letters: **M**elina, Merchant **K**ale, **R**oderika, **B**laidd, and **S**ellen.

**The maps physically connect:** walk east through the `>` opening halfway down Limgrave's right edge, then step east once more. You enter the `<` opening at Erdtree's left edge. Walk west through it to return. Both maps are accessible from the start; the boss is sealed until Melina finishes the main quest preparations.

## Visual effects

Open **V**, then choose a key and press Enter:

| Key | Effect |
| --- | --- |
| Q | Expanding golden level-up ring |
| W | Map shakes; a red boss symbol appears |
| E | Map reveals left to right |
| R | Falling rain |
| F | Colored firework sparkles |
| H | Green healing pulse |
| T | Toggle animations on/off for this session |
| X | Return to exploration |

These are visual previews: they do not award levels, heal HP, spawn combat encounters, or alter your save. Movement W is available in exploration; effect W is available only inside the V menu. Real level-ups, healing, map entry, the boss encounter, and victory also trigger effects. Animations last roughly one second. They use ANSI cursor movement and automatically skip when output is redirected. To disable them at launch on macOS: `RPG_NO_EFFECTS=1 uv run main.py`.

## Saving and continuing

TinyDB creates `elden_ring_save.json` beside `main.py`. It contains accounts and game progress. Each completed exploration action saves automatically; X and Ctrl+C during gameplay also save. If interrupted during combat, the enemy is not recorded as defeated and the fight starts fresh when encountered again. Keep the save file to keep your accounts.

A defeat returns you to Limgrave's Grace with full HP. Completed quests and defeated enemies remain saved. The game does not permanently lock you into a death state. A completed account remains won; register another account for a fresh playthrough.

The original project's save format is supported: plaintext account passwords are converted to salted hashes after a successful login. New fields receive defaults. Maps have changed, so an old character's coordinate may now refer to a different-looking location. For a clean assignment recording, use a new account. Back up your old save before transferring it into this folder.

## Assignment checklist

| Requirement | Implementation |
| --- | --- |
| Story intro and color | `main.py`, Colorama throughout |
| Registration/login; TinyDB | `auth.py`, `database.py`; salted password hashes |
| At least 10 meaningful Python files | 15 game modules, plus `test_game.py` |
| Five distinct NPCs | Melina, Kale, Roderika, Blaidd, Sellen |
| Multi-step main quest | Accept → collect 3 shards → return shards → break seal → defeat boss |
| Two rewarded side quests | Lost Keepsake: 30 gold + 30 XP; Clear the Road: Smithing Stone + 40 XP |
| Five monster types plus boss | Noble, Demi-Human, Soldier, Stray, Knight, Elden Lord |
| Monster gold and item drops | Each victory awards gold, XP, and a type-specific item |
| Shop and inventory | Buy/use consumables; buy/equip weapons; use attack buffs |
| Multiple learnable skills | Sellen teaches Flame of the Fell and Golden Vow; Heavy Strike is the starting skill |
| Different effects/cooldowns | Damage skills and healing; 1-, 2-, and 3-turn cooldowns |
| Character progression/status | HP, XP, level, gold, skills, inventory; press C |
| Two distinct maps with obstacles | Limgrave wetlands/ruins; shaped Erdtree corridors; bidirectional edge openings |
| Monster and Skill inheritance | Base classes and subclasses in `monster.py` / `skill.py` |
| Resume important progress | Stats, items, skills, coordinates, quests, cleared encounters, victory |
| Input validation/error handling | Invalid commands/indices rejected, save/load errors reported, interrupts handled |
