class Item:
    def __init__(self, name, description, price, item_type, power):
        self.name = name
        self.description = description
        self.price = price
        self.item_type = item_type
        self.power = power


ITEMS = {
    "Crimson Flask": Item("Crimson Flask", "Restores 35 HP.", 12, "heal", 35),
    "Golden Rune": Item("Golden Rune", "A small bundle of runes worth 25 gold.", 18, "gold", 25),
    "Smithing Stone": Item("Smithing Stone", "A useful upgrade token worth 20 XP.", 20, "xp", 20),
    "Fire Grease": Item("Fire Grease", "Adds fire power to your next attack.", 15, "buff", 15),
    "Great Rune Shard": Item("Great Rune Shard", "A rare quest relic.", 0, "quest", 0),
    "Rusty Sword": Item("Rusty Sword", "A simple weapon. Attack bonus +5.", 0, "weapon", 5),
    "Knight's Greatsword": Item("Knight's Greatsword", "A powerful weapon. Attack bonus +15.", 75, "weapon", 15),
    "Moonveil Fragment": Item("Moonveil Fragment", "A rare blade fragment. Attack bonus +12.", 60, "weapon", 12)
}
