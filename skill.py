class Skill:
    def __init__(self, name, description, cooldown):
        self.name = name
        self.description = description
        self.cooldown = cooldown

    def use(self, player, monster):
        return 0


class HeavyStrike(Skill):
    def __init__(self):
        super().__init__("Heavy Strike", "Deals 22 + 2 per level damage.", 1)

    def use(self, player, monster):
        return 22 + player.get("level") * 2


class FlameOfTheFell(Skill):
    def __init__(self):
        super().__init__("Flame of the Fell", "Deals 30 + level fire damage.", 2)

    def use(self, player, monster):
        return 30 + player.get("level")


class GoldenVow(Skill):
    def __init__(self):
        super().__init__("Golden Vow", "Restores 25 HP.", 3)

    def use(self, player, monster):
        player.heal(25)
        return 0


SKILLS = {
    "Heavy Strike": HeavyStrike(),
    "Flame of the Fell": FlameOfTheFell(),
    "Golden Vow": GoldenVow()
}


def learn_skill(player, skill_name):
    if skill_name in SKILLS and skill_name not in player.get("skills"):
        player.get("skills").append(skill_name)
        player.get("cooldowns")[skill_name] = 0
        return True
    return False
