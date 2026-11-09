class Player:
    def __init__(self, data):
        from auth import new_player_data
        self.data = new_player_data(data.get("name", "Tarnished"))
        self.data.update(data)
        self.data.setdefault("cleared", [])
        self.data.setdefault("keepsake_found", False)
        self.data.setdefault("road_cleared", False)
        self.data.setdefault("roderika_gift", False)
        self.data.setdefault("attack_buff", 0)

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value

    def take_damage(self, amount):
        self.data["hp"] = self.data["hp"] - amount
        if self.data["hp"] < 0:
            self.data["hp"] = 0
        if self.data["hp"] == 0:
            self.data["lost"] = True

    def heal(self, amount):
        from effects import play_effect
        play_effect(self, "heal")
        self.data["hp"] = self.data["hp"] + amount
        if self.data["hp"] > self.data["max_hp"]:
            self.data["hp"] = self.data["max_hp"]

    def gain_xp(self, amount):
        self.data["xp"] = self.data["xp"] + amount
        needed = self.data["level"] * 100
        while self.data["xp"] >= needed:
            self.data["xp"] = self.data["xp"] - needed
            self.data["level"] = self.data["level"] + 1
            self.data["max_hp"] = self.data["max_hp"] + 10
            self.data["hp"] = self.data["max_hp"]
            print("Level up! You are now level", self.data["level"])
            from effects import play_effect
            play_effect(self, "level")
            needed = self.data["level"] * 100

    def show_status(self):
        print("\n--- Tarnished Status ---")
        print("Name:", self.data["name"])
        print("Level:", self.data["level"])
        print("HP:", self.data["hp"], "/", self.data["max_hp"])
        print("XP:", self.data["xp"], "/", self.data["level"] * 100)
        print("Gold:", self.data["gold"])
        print("Weapon:", self.data["equipment"])
        print("Skills:", ", ".join(self.data["skills"]))
        print("Location:", self.data["map_name"])
        print("Main quest step:", self.data["main_quest"], "/ 4")
