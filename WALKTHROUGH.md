# Recording a complete playthrough

The map stays visible after every command. Use W/A/S/D plus Enter. Positions below use zero-based `(x, y)` coordinates; find the matching map letters and enemy markers visually. Obstacles require going around them.

## Recommended route

1. Start `uv run main.py`. Show the story. Register a new account and log in. Do not show a real reused password in your recording.
2. You begin on Grace at `(1,1)`, next to **M**elina `(2,1)`. Press **T** to accept Shattered Grace. Press **J** to show stage 1.
3. Visit **R**oderika `(2,6)`, press **T** for Lost Keepsake and a free flask. Visit **B**laidd `(5,9)`, press **T** for Clear the Road. You may finish their target fights before accepting; the game remembers them.
4. Fight all three Limgrave **!** encounters: Demi-Human `(5,3)`, Godrick Soldier `(10,4)`, and Wandering Noble `(15,7)`. Each drops one Great Rune Shard. Their gold/items and side-quest rewards are shown. Use Heavy Strike in combat; use a flask when needed. You can return to Grace `(1,1)` and press **G** for a free full heal between fights.
5. Press **I**, **J**, and **C** to show inventory, the completed side quests, and character progression. Use the Golden Rune through **U** to receive 25 gold. Use a Smithing Stone for XP if desired.
6. Visit **K**ale `(5,1)`, press **K**, and buy Knight's Greatsword for 75 gold when affordable. It auto-equips and also appears in your inventory. Buy extra Crimson Flasks for 12 gold each if needed.
7. Return to **M**elina. Press **T** once to deliver the three shards, then **T** again to break the boss seal. Press **J** to show the boss objective.
8. Walk to Limgrave's **>** at `(20,5)` and move east one additional step. The Erdtree map reveals. Walk west through **<** to demonstrate the return connection, then come back. Erdtree's Grace is `(2,5)`; stand there and press **G**.
9. Fight the Putrid Stray at `(7,5)` and Crucible Knight at `(12,3)` to show all five normal monster types. Return to Grace between fights if needed. These enemies are optional for the main quest but useful for the video and rewards.
10. To demonstrate learning, revisit **S**ellen in Limgrave `(16,9)`. Press **T** and buy Flame of the Fell (25 gold) and/or Golden Vow (40 gold). Each is a separate interaction. Press **C** to show learned skills and use them in a remaining fight. Save enough gold for healing supplies. If both optional encounters are already cleared, demonstrate skills in the boss fight.
11. Press **V** and demonstrate **Q, W, E, R, F, H**. Press **X** to return. These previews do not affect stats. Automatic animations also run during normal play.
12. Press **P**, then **X**. Answer `yes` to return to the title and log back in. Show that location, inventory, stats, and quests resume correctly.
13. Rest at Erdtree Grace and stock up before the final battle. Reach **D**, the Elden Lord, at `(18,1)`. Attack with the greatsword and use skills/flasks. You cannot flee from this boss. If defeated, you revive in Limgrave and can return without redoing quests.
14. Defeat the boss. Show the **YOU ARE ELDEN LORD! / YOU WIN!** message and saved victory.

A normal attack with Knight's Greatsword is stronger than Heavy Strike at some levels, so do not assume every skill always does more damage than an equipped weapon. Healing skills and flasks consume a combat turn. An enemy's special attack may hit harder than its normal attack; heal before HP gets dangerously low.

## Submit to GitHub

Use your own GitHub account and create a repository. Upload the contents of the project folder, including all `.py` files, `pyproject.toml`, `requirements.txt`, `.gitignore`, and the guides. Do not upload `elden_ring_save.json`, `.venv`, or `__pycache__`. If using GitHub's web uploader, explicitly leave those folders/files out; `.gitignore` primarily protects Git-based workflows.

Record your own gameplay from beginning to end and submit the repository link and video as your instructor specifies. This package does not publish a repository or create a recording for you.
