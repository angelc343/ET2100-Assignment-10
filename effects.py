"""Short ANSI animations. No threads, no changes to game state."""
import os
import random
import sys
import time
from colorama import Fore, Style
from world_map import MAPS, map_lines

ENABLED = True

def play_effect(player, effect):
    if not ENABLED or not sys.stdout.isatty() or os.getenv("RPG_NO_EFFECTS"):
        return
    rows = MAPS[player.get("map_name")]
    width, height = len(rows[0]), len(rows)
    px, py = player.get("x"), player.get("y")
    frames = width if effect == "reveal" else 10
    rng = random.Random()
    print("\033[?25l", end="")  # Hide cursor during frames only.
    try:
        for frame in range(frames):
            overlay = {}
            if effect in ("level", "heal") and frame < 9:
                radius = 1 + frame // 3
                for y in range(height):
                    for x in range(width):
                        if abs(x-px) + abs(y-py) == radius and rows[y][x] == ".":
                            overlay[(x,y)] = ("+" if effect == "heal" else "o",
                                (Fore.GREEN if effect == "heal" else Fore.YELLOW) + (Style.DIM if frame >= 6 else Style.BRIGHT))
            elif effect == "rain":
                for x in range(width):
                    y = (frame + x * 3) % height
                    if rows[y][x] == ".": overlay[(x,y)] = ("|", Fore.CYAN)
            elif effect == "firework":
                for _ in range(22):
                    x, y = rng.randrange(width), rng.randrange(height)
                    if rows[y][x] == ".":
                        overlay[(x,y)] = ("*", rng.choice([Fore.YELLOW, Fore.MAGENTA, Fore.CYAN]))
            elif effect == "boss" and frame >= 6:
                overlay[(px, max(0, py-1))] = ("D", Fore.RED)
            print("\033[2J\033[H", end="")
            print(Fore.YELLOW + "SHATTERED GRACE | " + effect.upper())
            indent = "  " if effect == "boss" and frame % 2 else ""
            for line in map_lines(player, overlay, frame if effect == "reveal" else None):
                print(indent + line)
            sys.stdout.flush()
            time.sleep(0.045 if effect == "reveal" else 0.09)
    finally:
        print("\033[?25h", end="", flush=True)

def effects_menu(player):
    global ENABLED
    while True:
        print("\nEffects demo: Q level ring | W boss shake | E reveal")
        print("R rain | F fireworks | H heal pulse | T toggle animations | X back")
        key = input("Effect + Enter: ").strip().lower()
        if key == "x": return
        if key == "t":
            ENABLED = not ENABLED
            print("Animations:", "on" if ENABLED else "off")
            continue
        effect = {"q":"level", "w":"boss", "e":"reveal", "r":"rain", "f":"firework", "h":"heal"}.get(key)
        if effect:
            play_effect(player, effect)
            from world_map import show_map
            show_map(player)
        else: print("Choose a listed effect.")
