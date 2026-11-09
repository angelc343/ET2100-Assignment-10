"""Five characters with different dialogue and useful interactions."""
from colorama import Fore
from skill import learn_skill, SKILLS
from quest import accept_side_quest, advance_main_quest

NPCS = {
    "Melina": "Follow grace, Tarnished. Three shards shall break the golden seal.",
    "Merchant Kale": "My wares may keep you alive. Press K nearby to trade.",
    "Roderika": "A Demi-Human stole my keepsake. Would you recover it?",
    "Blaidd": "A Godrick Soldier controls the road. Put an end to his watch.",
    "Sorceress Sellen": "A sharp mind can wield flame and mend broken flesh."
}

def talk_to_npc(player, npc_name):
    print(Fore.CYAN + npc_name + ": " + NPCS[npc_name])
    if npc_name == "Melina": advance_main_quest(player)
    elif npc_name == "Roderika":
        accept_side_quest(player, "Lost Keepsake")
        if not player.get("roderika_gift"):
            player.get("inventory").append("Crimson Flask")
            player.set("roderika_gift", True)
            print("Roderika gives you one Crimson Flask for the journey.")
    elif npc_name == "Blaidd": accept_side_quest(player, "Clear the Road")
    elif npc_name == "Sorceress Sellen":
        lessons = [("Flame of the Fell", 25), ("Golden Vow", 40)]
        for i, (name, price) in enumerate(lessons, 1):
            print(f"{i}. {name}: {price} gold. {SKILLS[name].description}")
        answer = input("Learn 1 or 2, or 0 to cancel: ").strip()
        if answer == "0": return
        if answer not in ("1", "2"):
            print("Choose 0, 1, or 2.")
            return
        name, price = lessons[int(answer)-1]
        if name in player.get("skills"): print("You already know that skill.")
        elif player.get("gold") < price: print("Not enough gold.")
        else:
            learn_skill(player, name)
            player.set("gold", player.get("gold")-price)
            print("Learned", name)
