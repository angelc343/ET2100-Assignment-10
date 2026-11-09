"""Two connected maps. Coordinates are (column, row), starting at zero."""
from colorama import Fore, Style

MAPS = {
    "Limgrave": [
        "#####################",
        "#.......#...........#",
        "#.......#..~~~......#",
        "#..........~~~..##..#",
        "#..###..............#",
        "#..#.....###.........",
        "#..#...........##...#",
        "#......~~~..........#",
        "#......~~~..###.....#",
        "#...................#",
        "#####################",
    ],
    "Erdtree": [
        "      ###############",
        "      #.............#",
        "  #####..###..###...#",
        "  #................##",
        "###..###....###....##",
        ".........#.........##",
        "###......#..###....##",
        "  #..##.............#",
        "  #####..###..###...#",
        "      #.............#",
        "      ###############",
    ],
}
NPC_LOCATIONS = {
    "Melina": (2, 1), "Merchant Kale": (5, 1),
    "Roderika": (2, 6), "Blaidd": (5, 9), "Sorceress Sellen": (16, 9),
}
NPC_SYMBOLS = dict(zip(NPC_LOCATIONS, "MKRBS"))
GRACES = {"Limgrave": (1, 1), "Erdtree": (2, 5)}
BOSS = (18, 1)
# Fixed encounters make the entire quest possible without random grinding.
ENCOUNTERS = {
    "Limgrave": {(5, 3): "DemiHuman", (10, 4): "GodrickSoldier",
                 (15, 7): "WanderingNoble"},
    "Erdtree": {(7, 5): "PutridStray", (12, 3): "CrucibleKnight"},
}

def encounter_id(map_name, x, y):
    return f"{map_name}:{x}:{y}"

def map_lines(player, overlay=None, reveal=None):
    """Return colored rows; animations may temporarily overlay visible cells."""
    name = player.get("map_name")
    rows = MAPS[name]
    overlay = overlay or {}
    output = []
    for y, row in enumerate(rows):
        line = ""
        for x, tile in enumerate(row):
            color = Fore.LIGHTBLACK_EX
            glyph = {"#": "#", ".": ".", "~": "~", " ": " "}[tile]
            if tile == ".": color = Fore.GREEN
            if tile == "~": color = Fore.BLUE
            if (x, y) == GRACES[name]: glyph, color = "*", Fore.YELLOW
            if name == "Limgrave":
                for npc, pos in NPC_LOCATIONS.items():
                    if pos == (x, y): glyph, color = NPC_SYMBOLS[npc], Fore.CYAN
            key = encounter_id(name, x, y)
            if (x, y) in ENCOUNTERS[name] and key not in player.get("cleared"):
                glyph, color = "!", Fore.RED
            if (name == "Limgrave" and (x, y) == (20, 5)):
                glyph, color = ">", Fore.YELLOW
            if (name == "Erdtree" and (x, y) == (0, 5)):
                glyph, color = "<", Fore.YELLOW
            if name == "Erdtree" and (x, y) == BOSS and not player.get("won"):
                glyph, color = "D", Fore.LIGHTRED_EX
            if (x, y) == (player.get("x"), player.get("y")):
                glyph, color = "@", Fore.WHITE + Style.BRIGHT
            if (x, y) in overlay: glyph, color = overlay[(x, y)]
            if reveal is not None and x > reveal: glyph = " "
            line += color + glyph + " " + Style.RESET_ALL
        output.append(line)
    return output

def show_map(player):
    print(Fore.YELLOW + "\n+--- " + player.get("map_name").upper() + " --- SHATTERED GRACE ---+")
    for line in map_lines(player): print(line)
    print("@ You   # Wall   ~ Water   * Grace   ! Enemy   D Boss")
    print("M Melina | K Kale | R Roderika | B Blaidd | S Sellen")
    print("Limgrave east > < Erdtree west (walk through the edge)")
    print(f"HP {player.get('hp')}/{player.get('max_hp')} | Level {player.get('level')} | Gold {player.get('gold')}")

def move_player(player, direction):
    steps = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
    if direction not in steps:
        print("Use W, A, S, or D.")
        return False
    dx, dy = steps[direction]
    x, y = player.get("x") + dx, player.get("y") + dy
    name = player.get("map_name")
    # Crossing the opening moves to the other map, with an opening back.
    if name == "Limgrave" and (x, y) == (21, 5):
        player.set("map_name", "Erdtree")
        player.set("x", 0)
        player.set("y", 5)
        return True
    if name == "Erdtree" and (x, y) == (-1, 5):
        player.set("map_name", "Limgrave")
        player.set("x", 20)
        player.set("y", 5)
        return True
    rows = MAPS[name]
    if not (0 <= y < len(rows) and 0 <= x < len(rows[y])) or rows[y][x] != ".":
        print("Stone, water, or the edge blocks that way.")
        return False
    player.set("x", x)
    player.set("y", y)
    return True
