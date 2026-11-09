"""Exploration connects maps, encounters, NPCs, menus, and autosaving."""
from colorama import Fore
from database import save_player
from player import Player
from world_map import (show_map, move_player, NPC_LOCATIONS, GRACES,
                       ENCOUNTERS, BOSS, encounter_id)
import monster as monsters
from combat import fight
from inventory import show_inventory, use_item
from shop import visit_shop
from npc import talk_to_npc
from quest import show_quests, complete_side_quest
from effects import play_effect, effects_menu

class Game:
    def __init__(self, data):
        data = dict(data)
        self.username = data.pop("username")
        self.player = Player(data)

    def save(self):
        save_player(self.username, self.player.data)

    def nearby_npc(self):
        if self.player.get("map_name") == "Limgrave":
            for name, (x, y) in NPC_LOCATIONS.items():
                if abs(x-self.player.get("x")) + abs(y-self.player.get("y")) <= 1:
                    return name
        return None

    def recover(self):
        if self.player.get("hp") <= 0 or self.player.get("lost"):
            self.player.set("lost", False)
            self.player.set("hp", self.player.get("max_hp"))
            self.player.set("map_name", "Limgrave")
            self.player.set("x", 1)
            self.player.set("y", 1)
            self.player.set("cooldowns", {})
            print("Grace revives you in Limgrave. Your quest progress is safe.")

    def encounter(self):
        p = self.player
        name, x, y = p.get("map_name"), p.get("x"), p.get("y")
        key = encounter_id(name, x, y)
        kind = ENCOUNTERS[name].get((x, y))
        if name == "Erdtree" and (x, y) == BOSS and not p.get("won"):
            if p.get("main_quest") < 3:
                print("The golden seal holds. Return three shards to Melina, then speak again.")
                return
            play_effect(p, "boss")
            if fight(p, monsters.EldenLord()):
                p.set("main_quest", 4)
                play_effect(p, "firework")
        elif kind and key not in p.get("cleared"):
            if fight(p, getattr(monsters, kind)()):
                p.get("cleared").append(key)
                if name == "Limgrave":
                    p.get("inventory").append("Great Rune Shard")
                    print("You recovered a Great Rune Shard! (One from each Limgrave enemy.)")
                if kind == "DemiHuman": p.set("keepsake_found", True)
                if kind == "GodrickSoldier": p.set("road_cleared", True)
                self.check_side_quests()
        self.recover()

    def check_side_quests(self):
        if self.player.get("keepsake_found"):
            complete_side_quest(self.player, "Lost Keepsake")
        if self.player.get("road_cleared"):
            complete_side_quest(self.player, "Clear the Road")

    def run(self):
        p = self.player
        self.recover()
        play_effect(p, "reveal")
        if p.get("won"):
            print("YOU ARE ELDEN LORD! This saved journey is complete.")
            return
        try:
            while not p.get("won"):
                show_map(p)
                print("W/A/S/D move | T talk | J quests | I inventory | U use/equip")
                print("C character | K shop | G rest at Grace | V effects | P save | X quit")
                cmd = input("Action + Enter: ").strip().lower()
                if cmd in ("w", "a", "s", "d"):
                    old_map = p.get("map_name")
                    if move_player(p, cmd):
                        if old_map != p.get("map_name"): play_effect(p, "reveal")
                        self.encounter()
                elif cmd == "t":
                    npc = self.nearby_npc()
                    if npc: talk_to_npc(p, npc)
                    else: print("Stand on or next to an NPC letter to talk.")
                elif cmd == "j": show_quests(p)
                elif cmd == "i": show_inventory(p)
                elif cmd == "u": use_item(p)
                elif cmd == "c": p.show_status()
                elif cmd == "k":
                    if self.nearby_npc() == "Merchant Kale": visit_shop(p)
                    else: print("Visit K (Merchant Kale) in Limgrave.")
                elif cmd == "g":
                    if (p.get("x"), p.get("y")) == GRACES[p.get("map_name")]:
                        p.heal(p.get("max_hp"))
                        p.set("cooldowns", {})
                        print("Restored at Grace. Enemies remain defeated.")
                    else: print("Stand on a golden * to rest.")
                elif cmd == "v": effects_menu(p)
                elif cmd == "p":
                    self.save()
                    print("Game saved.")
                elif cmd == "x": return
                else: print("Choose one of the listed commands.")
                self.check_side_quests()
                self.save()
            print(Fore.YELLOW + "YOU ARE ELDEN LORD! The throne is yours. YOU WIN!")
        except (KeyboardInterrupt, EOFError):
            print("\nLeaving the Lands Between.")
        finally:
            self.recover()
            self.save()
