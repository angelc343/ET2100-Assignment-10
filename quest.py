from colorama import Fore


def show_quests(player):
    step = player.get("main_quest")
    steps = [
        "Speak with Melina and accept the quest.",
        "Defeat enemies and collect 3 Great Rune Shards.",
        "Return to Melina with the shards.",
        "Travel to the Erdtree and defeat the Elden Lord.",
        "Complete! You are Elden Lord."
    ]
    print(Fore.YELLOW + "\n--- Main Quest: Shattered Grace ---")
    print("Current step:", steps[step])
    print("\nSide quests:")
    print("1. Lost Keepsake - defeat a Demi-Human; reward 30 gold and 30 XP.")
    print("2. Clear the Road - defeat a Godrick Soldier; reward a Smithing Stone and 40 XP.")
    print("Active side quests:", ", ".join(player.get("side_quests")) or "None")
    print("Shards:", player.get("inventory").count("Great Rune Shard"), "/ 3")
    print("Completed side quests:", ", ".join(player.get("completed_side_quests")) or "None")


def accept_side_quest(player, quest_name):
    if quest_name not in player.get("side_quests") and quest_name not in player.get("completed_side_quests"):
        player.get("side_quests").append(quest_name)
        print("Quest accepted:", quest_name)
    else:
        print("You already accepted or completed that quest.")


def complete_side_quest(player, quest_name):
    if quest_name not in player.get("side_quests"):
        return
    if quest_name == "Lost Keepsake":
        player.set("gold", player.get("gold") + 30)
        player.gain_xp(30)
    elif quest_name == "Clear the Road":
        player.get("inventory").append("Smithing Stone")
        player.gain_xp(40)
    player.get("side_quests").remove(quest_name)
    player.get("completed_side_quests").append(quest_name)
    print(Fore.GREEN + "Side quest complete:", quest_name)


def advance_main_quest(player):
    step = player.get("main_quest")
    if step == 0:
        player.set("main_quest", 1)
        print("Melina entrusts you with the hunt for Great Rune Shards.")
    elif step == 1:
        shards = player.get("inventory").count("Great Rune Shard")
        if shards >= 3:
            for i in range(3):
                player.get("inventory").remove("Great Rune Shard")
            player.set("main_quest", 2)
            print("You return the three shards to Melina.")
        else:
            print("You need 3 Great Rune Shards. Explore and defeat powerful enemies.")
    elif step == 2:
        player.set("main_quest", 3)
        print("Melina breaks the boss seal. Walk east through > to reach the Erdtree.")
    else:
        print("The final path is open. Find the Elden Lord and defeat it.")
