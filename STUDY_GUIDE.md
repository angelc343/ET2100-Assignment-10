# Understanding the code for Midterm 2

Read the actual Python files along with this guide. Be able to explain each change in player state and why it is saved.

## 1. Overall design

`main.py` displays the story, calls registration/login, and creates a `Game`. `Game.run()` repeatedly displays the map, asks for a command, calls the appropriate system, and saves. This loop ends when the player quits or wins.

The program separates responsibilities:

| Module | What to understand |
| --- | --- |
| `main.py` | Entry point, story, title loop, top-level error reporting |
| `auth.py` | Starting character dictionary, registration, login |
| `database.py` | TinyDB reads/writes and password checking |
| `game.py` | Exploration loop, NPC proximity, encounters, death recovery |
| `world_map.py` | Grid data, colored rendering, collision checks, connected edges |
| `effects.py` | Temporary animation overlays and timing |
| `player.py` | Character dictionary, damage, healing, XP, levels |
| `monster.py` | Monster inheritance, stats, drops, special attacks |
| `skill.py` | Skill inheritance, damage/healing methods, learning |
| `combat.py` | Turn loop, input validation, cooldowns, victory rewards |
| `item.py` | Item objects and shared item catalog |
| `inventory.py` | Index validation, consumption, equipping, attack buffs |
| `npc.py` | Different dialogue, quests, lessons, one-time gift |
| `quest.py` | Main quest stages and once-only side quest rewards |
| `shop.py` | Purchase validation, gold deduction, adding/equipping items |
| `test_game.py` | Temporary-save tests, map pathfinding, full progression check |

Imports let one file reuse definitions from another. `Game` coordinates systems, so individual modules do not all need their own exploration loop.

## 2. How TinyDB stores and restores data

A player is a Python dictionary. Keys are strings such as `"hp"`, `"level"`, `"inventory"`, and `"main_quest"`. Values are integers, strings, booleans, lists, and dictionaries. These types can be represented by JSON, TinyDB's storage format.

A simplified TinyDB file looks like this (the hash and salt values here are explanatory placeholders):

```json
{
  "_default": {
    "1": {
      "username": "student",
      "salt": "hexadecimal random salt",
      "password_hash": "hexadecimal derived hash",
      "player": {
        "name": "Tarnished",
        "hp": 100,
        "level": 1,
        "xp": 0,
        "gold": 25,
        "inventory": ["Crimson Flask", "Rusty Sword"],
        "skills": ["Heavy Strike"],
        "cooldowns": {},
        "map_name": "Limgrave",
        "x": 1,
        "y": 1,
        "main_quest": 0,
        "side_quests": [],
        "completed_side_quests": [],
        "cleared": [],
        "won": false
      }
    }
  }
}
```

The real player dictionary includes additional fields. TinyDB owns the outer `_default` table and document IDs. Do not replace its file with a plain list of dictionaries: that is a different JSON structure.

`Accounts = Query()` constructs a query object. `Accounts.username == username` describes the matching account. `db.get(...)` reads it. `db.insert(...)` creates an account. `db.update({"player": player_data}, ...)` replaces only that account's nested player value, keeping its password information.

The `with open_db() as db:` block closes the database after each operation. The default path is beside `database.py`, so launching from a different directory does not create an unrelated save.

On login, the saved player dictionary is returned with the username. `Game` separates the username from character data. `Player` starts with defaults and updates them using the saved values, allowing older saves to receive newly introduced fields. Skill objects are not saved: their names are saved and used to look up the matching object in `SKILLS`.

**Check yourself:** Why save `"Golden Vow"` instead of a `GoldenVow()` instance? Because the name is JSON-compatible and the shared skill catalog can recreate the behavior.

## 3. Registration and login

Registration rejects a blank or existing username and a blank password. It creates a starting player dictionary. `os.urandom(16)` provides a random salt. `hashlib.pbkdf2_hmac` combines password and salt through repeated hashing. The database stores the salt and derived hash, not a new account's plaintext password.

Login searches for the username, derives a hash from the entered password using the stored salt, and compares hashes with `hmac.compare_digest`. If they match, the saved character is returned. `getpass()` hides password typing in a normal terminal. These standard-library security helpers are more advanced than the basic game logic; understand their purpose without needing to implement the cryptography yourself.

For older project saves containing `password`, a successful match replaces that field with a salt/hash pair. Wrong passwords do not migrate the account. This is a local classroom account system, not a hosted multiplayer service.

## 4. Inheritance

`Monster` is the parent class. Its constructor assigns shared attributes such as name, HP, attack damage, gold, XP, and item drops. `DemiHuman(Monster)` and `EldenLord(Monster)` inherit these attributes and methods. Their `super().__init__(...)` calls supply different stats.

`EldenLord.special_move()` overrides the inherited method: it adds damage instead of returning the ordinary base damage. `isinstance(monster, EldenLord)` identifies the final boss so combat can prevent escape and set the win flags.

`Skill` is the other parent class. Each subclass defines `use(player, monster)`:

- `HeavyStrike` returns `22 + level * 2` damage, cooldown 1.
- `FlameOfTheFell` returns `30 + level` damage, cooldown 2.
- `GoldenVow` restores 25 HP and returns zero damage, cooldown 3.

Combat calls the same method name on different skill objects. The subclass determines the behavior. That is polymorphism.

## 5. Quest state

`main_quest` is an integer representing a stage:

| Value | Meaning / next action |
| --- | --- |
| 0 | Talk to Melina to accept |
| 1 | Collect three Great Rune Shards and return them |
| 2 | Shards delivered; speak to Melina again to break the seal |
| 3 | Enter Erdtree and defeat the boss |
| 4 | Victory |

Each of the three fixed Limgrave enemies drops one shard on its first defeat. `cleared` stores strings such as `"Limgrave:5:3"`, preventing repeated enemy rewards. Returning shards removes exactly three from the inventory. Talking again changes stage 2 to 3; it does not teleport the player. The player walks through the physical connection.

Side quests use two lists: active quest names and completed quest names. Roderika and Blaidd add their quests to the active list. `keepsake_found` and `road_cleared` record the relevant kills even if the player accepts the quest later. Completion checks require an active quest, give its reward, remove it from active, and add it to completed. Calling the check again cannot give a duplicate reward.

## 6. Maps, movement, and encounters

Each map is a list of strings. A row is selected by `y`; a character within that row is selected by `x`: `MAPS[name][y][x]`. Coordinates start at zero. W reduces y; S increases y; A reduces x; D increases x.

Movement first calculates a proposed position. The two explicit edge-crossing cases change the map name and place the player at the matching opening. Other moves must remain in bounds and target a `.` ground tile. Walls, water, and blank space are blocked. Invalid movement leaves coordinates unchanged.

NPCs, Grace, enemies, the boss, and the player are overlays on the base map. Their underlying cells remain walkable. The renderer draws them in a consistent order, with the player drawn last so `@` remains visible. NPC interaction uses Manhattan distance: `abs(dx) + abs(dy) <= 1`, meaning the same cell or an orthogonally adjacent cell.

A successful move calls `encounter()`. If the destination contains an uncleared enemy, it starts combat. A defeated enemy is added to `cleared`; escaping or losing does not clear it. The final boss checks the main quest stage before combat begins.

## 7. Combat, items, progression, and cooldowns

Combat loops while both combatants have positive HP. Normal attacks use level and weapon bonuses. Fire Grease adds damage to the next normal attack, then clears its stored bonus. Successful skill use applies its subclass effect. Invalid commands, unavailable skills, and canceled/invalid items do not give the enemy a free turn.

An item action returns `True` only when something actually happens. Consumables are removed; equipment remains owned. Shopping rejects negative or out-of-range indices and checks gold before buying.

After a valid action, a living enemy attacks. It has a 20% chance to use `special_move()`. Skill cooldowns decrease after a completed nonlethal player action. A newly used skill starts at its cooldown plus one, because that round immediately decrements it. Heavy Strike therefore requires one intervening action before reuse. Cooldowns reset at the start of each battle and at Grace.

Victory gives gold, XP, and the enemy's item. `gain_xp()` uses a `while` loop so one large reward can grant more than one level. Each level needs `level * 100` XP; leftover XP carries over. Leveling increases max HP by 10 and fully heals.

Defeat sets HP to zero. `Game.recover()` revives the character at Limgrave's Grace, restores HP, and clears the lost flag. Quest progress and inventory survive. The boss victory sets `won` and `boss_defeated`; the controller sets stage 4 and ends the game.

## 8. Effects

`effects.py` creates short sequences of frames. Every frame redraws the map with temporary glyphs placed in an overlay dictionary. A ring uses Manhattan distance around the player. Rain changes vertical positions each frame. The reveal limits visible columns. The boss shake alternates indentation. Fireworks use random colored stars.

`time.sleep()` briefly pauses between frames. ANSI escape sequences clear the screen and hide/show the cursor. The `finally` block restores cursor visibility even if an animation is interrupted. Effects do not modify player stats or base map data. `isatty()` prevents control sequences from being used as animation when output is redirected.

## Practice questions

1. What happens from pressing T next to Melina to saving the new quest stage?
2. Which fields must change when crossing from Limgrave to Erdtree?
3. Why does Python index `-1` need to be rejected in a numbered menu?
4. How do completed side quests prevent duplicate rewards?
5. What does `super().__init__()` do in a monster subclass?
6. How can one `skill.use(...)` call either damage an enemy or heal the player?
7. Why does the XP calculation use `while` instead of `if`?
8. What remains saved if you quit after a battle and log back in?
9. Why must TinyDB's JSON table structure remain intact?
10. What is the difference between an animation overlay and saved game state?
