class Monster:
    def __init__(self, name, hp, damage, gold_drop, xp_drop, item_drop=None):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.gold_drop = gold_drop
        self.xp_drop = xp_drop
        self.item_drop = item_drop

    def attack(self):
        return self.damage

    def special_move(self):
        return self.damage


class WanderingNoble(Monster):
    def __init__(self):
        super().__init__("Wandering Noble", 28, 7, 8, 20, "Crimson Flask")


class DemiHuman(Monster):
    def __init__(self):
        super().__init__("Demi-Human", 38, 9, 12, 30, "Golden Rune")


class GodrickSoldier(Monster):
    def __init__(self):
        super().__init__("Godrick Soldier", 48, 11, 15, 40, "Smithing Stone")


class PutridStray(Monster):
    def __init__(self):
        super().__init__("Putrid Stray", 42, 13, 18, 45, "Fire Grease")


class CrucibleKnight(Monster):
    def __init__(self):
        super().__init__("Crucible Knight", 65, 15, 25, 60, "Moonveil Fragment")


class EldenLord(Monster):
    def __init__(self):
        super().__init__("Elden Lord", 150, 18, 100, 200, "Great Rune Shard")

    def special_move(self):
        return self.damage + 8


def random_monster():
    import random
    monsters = [WanderingNoble, DemiHuman, GodrickSoldier, PutridStray, CrucibleKnight]
    return random.choice(monsters)()
